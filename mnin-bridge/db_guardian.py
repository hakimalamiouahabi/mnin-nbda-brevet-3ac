"""MNIN Bridge DBGuardian: inventory and safe maintenance planning, NEVER cleanup execution.

All database access is read-only, local and restricted to MNIN_DB_AUDIT_ROOT.
A Cloudflare D1 database must be *separately* exported through authorized tools.
Do not feed production personal data into this module or a public GitHub repo.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
from pathlib import Path
from urllib.parse import quote

ALLOWED_EXTENSIONS = {".sqlite", ".sqlite3", ".db"}
SIMPLE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,159}$")
PROTECTED = (
    "user", "account", "student", "parent", "finance", "payment",
    "order", "audit", "security", "session", "subscription",
    "entitlement", "consent", "verification", "ledger", "identity",
    "credential", "token", "profile", "event", "invoice"
)
CACHE_WORDS = ("cache", "temporary", "temp_", "transient", "rate_limit", "ratelimit")
EXPIRY_COLUMNS = {"expires", "expires_at", "expires_on", "expiresat",
                  "expires_at_ms", "expireson", "expiration", "ttl"}
ALLOWED_REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def maintenance_guardrails() -> dict:
    """Read reviewed safety ceilings. An editable JSON file NEVER enables execution."""
    path=Path(__file__).with_name("maintenance") / "guardrails.json"
    rule=json.loads(path.read_text(encoding="utf-8"))
    if rule.get("schema_version") != "1.0" or rule.get("mode") != "READ_ONLY":
        raise RuntimeError("Unsupported or write-enabled DBGuardian guardrails")
    stages=rule.get("phase_gates",{})
    for key in ("backup","execute_staging","execute_production"):
        if stages.get(key,{}).get("allowed") is not False:
            raise RuntimeError("Unexpected mutable DBGuardian phase enabled")
    g=rule.get("guardrails",{})
    if g.get("max_parallel_write_workers") != 0 or g.get("dry_run_default") is not True:
        raise RuntimeError("Read-only maintenance constraints missing")
    if g.get("every_write_requires_independent_approval") is not True:
        raise RuntimeError("Owner authorization requirement missing")
    return rule


def _audit_root() -> Path:
    root = os.getenv("MNIN_DB_AUDIT_ROOT", "")
    if not root:
        raise RuntimeError("MNIN_DB_AUDIT_ROOT is required")
    path = Path(root).expanduser().resolve(strict=True)
    if not path.is_dir():
        raise ValueError("Audit root must be a directory")
    return path


def _approved_db(filename: str) -> Path:
    if not isinstance(filename, str) or not SIMPLE_NAME.fullmatch(filename):
        raise ValueError("Only a simple database filename is allowed")
    if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported database file extension")
    root = _audit_root()
    path = (root / filename).resolve(strict=True)
    if path.parent != root or not path.is_file():
        raise ValueError("Database must be located directly inside the approved folder")
    if path.stat().st_size > 200 * 1024 * 1024:
        raise ValueError("Snapshot larger than 200 MB; use separate approved audit")
    return path


def _quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def audit_sqlite_snapshot(filename: str) -> dict:
    """Read an approved SQLite snapshot without returning row-level personal data."""
    path = _approved_db(filename)
    # SQLite URI and query_only protect the audit even if a query is changed later.
    uri = "file:" + quote(str(path), safe="/") + "?mode=ro"
    with sqlite3.connect(uri, uri=True, timeout=5) as db:
        db.execute("PRAGMA query_only=ON")
        check = db.execute("PRAGMA quick_check(1)").fetchone()[0]
        page_size = db.execute("PRAGMA page_size").fetchone()[0]
        page_count = db.execute("PRAGMA page_count").fetchone()[0]
        freelist = db.execute("PRAGMA freelist_count").fetchone()[0]
        names = [row[0] for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name LIMIT 501")]
        if len(names) > 500:
            raise ValueError("More than 500 tables: manual audit required")
        tables = []
        for name in names:
            quoted = _quote_identifier(name)
            columns = [str(r[1]) for r in db.execute("PRAGMA table_info(" + quoted + ")")]
            indexes = [str(r[1]) for r in db.execute("PRAGMA index_list(" + quoted + ")")]
            foreign_keys = sum(1 for _ in db.execute("PRAGMA foreign_key_list(" + quoted + ")"))
            sensitive = any(word in name.lower() for word in PROTECTED)
            is_cache = any(word in name.lower() for word in CACHE_WORDS)
            expiry = [c for c in columns if c.lower() in EXPIRY_COLUMNS]
            category = ("protected" if sensitive else
                        "review_cache_candidate" if is_cache and expiry else
                        "unclassified")
            tables.append({"name":name, "columns":len(columns),
                           "indexes":len(indexes), "declared_foreign_keys":foreign_keys,
                           "category":category, "expiry_columns":expiry,
                           "action":"AUDIT_ONLY"})
    return {
        "filename":path.name,
        "bytes":path.stat().st_size,
        "integrity_quick_check":check,
        "page_size":page_size,
        "page_count":page_count,
        "freelist_count":freelist,
        "freelist_ratio":round(freelist/page_count, 4) if page_count else 0,
        "table_count":len(tables),
        "tables":tables,
        "data_values_exposed":False,
        "write_operations_performed":0,
        "recommendation":"No automatic purge; validate backups and table ownership first.",
        "notes":[
            "Freelist pages are not evidence of deletable business records.",
            "TTL column names do not prove that records have expired.",
            "SQLITE VACUUM and optimization may lock/replace files; review separately.",
        ],
    }


def preview_cleanup(context: str, candidates: list[dict], backup_verified: bool = False) -> dict:
    """Return a triage report: ALWAYS non-executing, even if backup_verified=True."""
    if context not in {"cloudflare_d1", "wordpress", "github"}:
        raise ValueError("Unsupported cleanup environment")
    if not isinstance(candidates, list) or len(candidates) > 200:
        raise ValueError("Invalid or too many candidates")
    normalized = []
    for c in candidates:
        if not isinstance(c, dict):
            raise ValueError("Candidate must be an object")
        label = c.get("name")
        if not isinstance(label, str) or not 1 <= len(label) <= 160:
            raise ValueError("Candidate must have a short name")
        kind = c.get("kind", "unknown")
        if kind not in {"transient_expired", "cache_ttl", "unused_index",
                        "stale_branch", "workflow_artifact", "revision",
                        "unused_asset", "other"}:
            raise ValueError("Unsupported cleanup category")
        risk = "HIGH" if (kind in {"other","stale_branch","revision"} or
                          any(s in label.lower() for s in PROTECTED)) else "REVIEW"
        normalized.append({
            "name":label,
            "kind":kind,
            "risk":risk,
            "action":"REVIEW_ONLY",
            "requires_backup":context in {"cloudflare_d1","wordpress"},
            "requires_separate_owner_approval":True,
        })
    return {
        "context":context,
        "dry_run":True,
        "backup_verified_by_caller":bool(backup_verified),
        "has_server_backup_proof":False,
        "candidates_count":len(normalized),
        "candidates":normalized,
        "write_operations_performed":0,
        "automatic_cleanup_allowed":False,
        "next_step":"Verify export/restore, dependencies, retention and explicit target approvals.",
    }


def wordpress_readonly_plan() -> dict:
    return {
        "site":"WordPress staging / separately selected",
        "read_only_checks":[
            "Backup success and restore preflight",
            "Total pages/posts/revisions, orphan attachments and database size",
            "Expired transients (NOT all transients)",
            "Unused plugins/themes only after dependency assessment",
            "Autoloaded options size (exclude secrets and personal contents)",
        ],
        "suggested_commands_for_human_review":[
            "wp db check",
            "wp transient list --format=count",
            "wp db size",
            "wp option list --autoload=on --fields=option_name,size_bytes --format=csv",
        ],
        "blocked_until_backup_and_approval":[
            "wp transient delete --expired",
            "wp db optimize",
            "any revision/media deletion",
            "plugin/theme deactivation or uninstall",
        ],
        "never_auto_run":["wp db clean","wp db drop","wp db reset","wp transient delete --all"],
        "executed_commands":0,
    }


def github_readonly_plan(repository: str) -> dict:
    if not isinstance(repository, str) or not ALLOWED_REPO.fullmatch(repository):
        raise ValueError("Unsafe repository name")
    return {
        "repository":repository,
        "read_only_checks":[
            "Stale branches with merged status and explicit branch protections",
            "Large Git objects using git-sizer on an isolated clone",
            "GitHub Actions artifact inventory and retention",
            "Dependabot/CI status and suspected exposed credentials via Gitleaks",
        ],
        "blocked_until_review":[
            "Pruning merged remote branches",
            "Changing CI artifact retention",
            "Rewriting Git history with git-filter-repo",
            "Deleting releases or tags",
        ],
        "never_auto_run":["git push --force","git push --mirror","git filter-repo on the only source copy"],
        "executed_commands":0,
    }


def cloudflare_readonly_plan(db_name: str) -> dict:
    if not isinstance(db_name, str) or not SIMPLE_NAME.fullmatch(db_name):
        raise ValueError("Unsafe database identifier")
    return {
        "database":db_name,
        "read_only_checks":[
            "List tables and indexes, excluding row values",
            "Inspect storage metrics and relevant constraints",
            "Determine actual D1 Time Travel window and current bookmark",
            "Export a restorable SQL snapshot to private storage",
            "Review TTL fields and consumer dependencies before any candidate purge",
        ],
        "blocked_until_review":[
            "DELETE/UPDATE or TRUNCATE",
            "VACUUM/REINDEX/PRAGMA optimize",
            "Migrations or schema changes",
            "Time Travel restore (overwrites database)",
        ],
        "executed_queries":0,
        "note":"D1 is SQLite, not the WordPress MySQL/MariaDB database.",
    }
