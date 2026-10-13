"""DBGuardian v0.7 unit tests — offline, no Cloudflare, GitHub or WordPress writes."""
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from db_guardian import (
    audit_sqlite_snapshot, preview_cleanup, wordpress_readonly_plan,
    github_readonly_plan, cloudflare_readonly_plan, maintenance_guardrails,
)


class DBGuardianTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        env=patch.dict(os.environ, {"MNIN_DB_AUDIT_ROOT":self.temp.name})
        env.start()
        self.addCleanup(env.stop)
        dbfile=self.root/"sample.sqlite3"
        with sqlite3.connect(dbfile) as db:
            db.execute("CREATE TABLE student_profiles(id INTEGER PRIMARY KEY, email TEXT)")
            db.execute("INSERT INTO student_profiles(email) VALUES ('test-private@example.invalid')")
            db.execute("CREATE TABLE cache_ttl(id INTEGER PRIMARY KEY, expires_at INT, payload TEXT)")
            db.execute("INSERT INTO cache_ttl(expires_at,payload) VALUES (100, 'private-value')")
            db.execute("CREATE TABLE lessons(id INTEGER PRIMARY KEY,title TEXT)")
            db.execute("CREATE INDEX idx_lessons_title ON lessons(title)")

    def test_readonly_schema_inventory(self):
        result=audit_sqlite_snapshot("sample.sqlite3")
        self.assertEqual(result["integrity_quick_check"],"ok")
        self.assertEqual(result["table_count"],3)
        self.assertEqual(result["write_operations_performed"],0)
        self.assertFalse(result["data_values_exposed"])
        names={t["name"]:t for t in result["tables"]}
        self.assertEqual(names["student_profiles"]["category"],"protected")
        self.assertEqual(names["cache_ttl"]["category"],"review_cache_candidate")
        self.assertEqual(names["lessons"]["category"],"unclassified")
        self.assertEqual(names["cache_ttl"]["action"],"AUDIT_ONLY")

    def test_does_not_return_private_row_contents(self):
        result=str(audit_sqlite_snapshot("sample.sqlite3"))
        self.assertNotIn("test-private@example.invalid",result)
        self.assertNotIn("private-value",result)

    def test_does_not_change_local_database_bytes(self):
        src=self.root/"sample.sqlite3"
        previous=src.read_bytes()
        audit_sqlite_snapshot("sample.sqlite3")
        self.assertEqual(src.read_bytes(),previous)

    def test_sensitive_cache_like_name_is_protected(self):
        with sqlite3.connect(self.root/"sample.sqlite3") as db:
            db.execute("CREATE TABLE user_session_cache(id INT, expires_at INT)")
        found={t["name"]:t for t in audit_sqlite_snapshot("sample.sqlite3")["tables"]}
        self.assertEqual(found["user_session_cache"]["category"],"protected")

    def test_no_root_denied(self):
        with patch.dict(os.environ,{"MNIN_DB_AUDIT_ROOT":""}):
            with self.assertRaises(RuntimeError):
                audit_sqlite_snapshot("sample.sqlite3")

    def test_unapproved_path_denied(self):
        for file in ("../sample.sqlite3","sub/sample.sqlite3","/tmp/sample.sqlite3","sample.txt"):
            with self.subTest(file=file):
                with self.assertRaises(ValueError):
                    audit_sqlite_snapshot(file)

    def test_symlink_external_denied(self):
        with tempfile.TemporaryDirectory() as external:
            outside=Path(external)/"external.sqlite3"
            with sqlite3.connect(outside) as db:
                db.execute("CREATE TABLE x(id)")
            shortcut=self.root/"symlink.sqlite3"
            try:
                shortcut.symlink_to(outside)
            except OSError:
                self.skipTest("symlink unavailable")
            with self.assertRaises(ValueError):
                audit_sqlite_snapshot(shortcut.name)

    def test_invalid_database_rejected(self):
        (self.root/"notdb.db").write_bytes(b"not database")
        with self.assertRaises(sqlite3.DatabaseError):
            audit_sqlite_snapshot("notdb.db")

    def test_preview_never_executes(self):
        result=preview_cleanup("wordpress",[{"name":"expired_transients","kind":"transient_expired"}],True)
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["write_operations_performed"],0)
        self.assertFalse(result["automatic_cleanup_allowed"])
        self.assertFalse(result["has_server_backup_proof"])
        self.assertTrue(result["candidates"][0]["requires_separate_owner_approval"])

    def test_preview_protects_finance(self):
        r=preview_cleanup("cloudflare_d1",[{"name":"finance_ledger","kind":"cache_ttl"}])
        self.assertEqual(r["candidates"][0]["risk"],"HIGH")

    def test_preview_all_three_contexts(self):
        for kind in ("cloudflare_d1","wordpress","github"):
            with self.subTest(context=kind):
                self.assertTrue(preview_cleanup(kind,[])["dry_run"])

    def test_preview_invalid_context_denied(self):
        with self.assertRaises(ValueError):
            preview_cleanup("production-delete",[{"name":"x","kind":"other"}])

    def test_preview_unknown_action_denied(self):
        with self.assertRaises(ValueError):
            preview_cleanup("wordpress",[{"name":"db_drop","kind":"truncate"}])

    def test_preview_excessive_candidates_denied(self):
        with self.assertRaises(ValueError):
            preview_cleanup("github",[{"name":f"branch-{i}","kind":"stale_branch"} for i in range(201)])

    def test_wordpress_forbids_dangerous_operations(self):
        p=wordpress_readonly_plan()
        self.assertIn("wp db drop",p["never_auto_run"])
        self.assertIn("wp transient delete --all",p["never_auto_run"])
        self.assertEqual(p["executed_commands"],0)

    def test_github_disallows_force_push(self):
        p=github_readonly_plan("example/repo")
        self.assertIn("git push --force",p["never_auto_run"])
        self.assertEqual(p["executed_commands"],0)

    def test_github_invalid_repository_denied(self):
        for r in ("a/../../b","https://github.com/x/y","foo",""):
            with self.assertRaises(ValueError):
                github_readonly_plan(r)

    def test_cloudflare_plan_read_only(self):
        p=cloudflare_readonly_plan("mnin-nbda-staging")
        self.assertIn("DELETE/UPDATE or TRUNCATE",p["blocked_until_review"])
        self.assertEqual(p["executed_queries"],0)

    def test_cloudflare_bad_database_denied(self):
        with self.assertRaises(ValueError):
            cloudflare_readonly_plan("../production")

    def test_guardrails_have_staging_only_scope(self):
        p=maintenance_guardrails()
        self.assertEqual(p["mode"],"READ_ONLY")
        self.assertEqual(p["scope"]["cloudflare_d1_allowlist"],["mnin-nbda-staging"])
        self.assertTrue(p["scope"]["external_projects_excluded"])

    def test_guardrails_disallow_deleting_and_parallel_writes(self):
        p=maintenance_guardrails()
        self.assertEqual(p["guardrails"]["max_parallel_write_workers"],0)
        self.assertTrue(p["guardrails"]["every_write_requires_independent_approval"])
        self.assertFalse(p["phase_gates"]["execute_staging"]["allowed"])
        self.assertFalse(p["phase_gates"]["execute_production"]["allowed"])

    def test_guardrails_require_restorable_backup(self):
        p=maintenance_guardrails()
        self.assertTrue(p["guardrails"]["backup_and_restore_preflight_required"])
        self.assertTrue(p["guardrails"]["stop_on_missing_backup"])
        self.assertIn("wp db drop",p["guardrails"]["prevent_wordpress_commands"])


if __name__=="__main__":
    unittest.main()
