"""Unit tests for MNIN Bridge mission proposal control-plane.

Run: python3 -m unittest discover -s mnin-bridge/tests -v
No real network, paid service, agent or WordPress access required.
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mission_control import MissionStore, capability_catalog, validate_request


class MissionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = MissionStore(self.tmp.name)
        self.home = {"branch": "feature/chemin-lumineux", "home_path": "site/index.html"}

    def test_capability_catalog_is_never_marked_active(self):
        result = capability_catalog()
        self.assertEqual(result["execution"], "NO RUNNER ACTIVATED")
        self.assertFalse(result["wordpress_writes"])
        self.assertFalse(result["model_api_charges"])
        self.assertEqual(len(result["capabilities"]), 5)

    def test_valid_requests(self):
        self.assertEqual(validate_request("home_browser_qa", self.home), self.home)
        self.assertEqual(validate_request("asset_integrity", {"filename":"amine.png"}),
                         {"filename":"amine.png"})

    def test_reject_arbitrary_executables_urls_and_extra_parameters(self):
        for kind, payload in [
            ("remote_shell", {"command": "rm -rf /"}),
            ("home_browser_qa", {"branch":"main","home_path":"site/index.html"}),
            ("home_browser_qa", {"branch":"feature/a", "home_path":"../../etc/passwd"}),
            ("home_browser_qa", {"branch":"feature/a","home_path":"https://example.net/x.html"}),
            ("home_browser_qa", {**self.home,"shell":"whoami"}),
            ("asset_integrity", {"filename":"../mine.png"}),
            ("asset_integrity", {"filename":"/tmp/key.png"}),
            ("asset_integrity", {"filename":"key.txt"}),
        ]:
            with self.subTest(kind=kind, payload=payload):
                with self.assertRaises(ValueError):
                    validate_request(kind, payload)

    def test_propose_is_not_execute(self):
        mission = self.store.propose("home_browser_qa", self.home)
        self.assertEqual(mission["status"], "PLANNED")
        self.assertEqual(mission["kind"], "home_browser_qa")
        events = self.store.audit(mission["mission_id"])
        self.assertEqual(events[0]["action"], "proposed")
        self.assertIn("No execution", events[0]["detail"])

    def test_read_list_and_preview(self):
        mission = self.store.propose("home_browser_qa", self.home)
        ident = mission["mission_id"]
        self.assertEqual(self.store.read(ident), mission)
        self.assertEqual(len(self.store.list()), 1)
        preview = self.store.preview(ident)
        self.assertFalse(preview["execution_possible_now"])
        self.assertEqual(preview["roles_spawned"], 0)
        self.assertIn("QA_AUTOMATION", preview["roles_requested"])

    def test_idempotency_same_request(self):
        first = self.store.propose("home_browser_qa", self.home, "home-test-01")
        second = self.store.propose("home_browser_qa", self.home, "home-test-01")
        self.assertEqual(first["mission_id"], second["mission_id"])
        self.assertEqual(len(self.store.list()), 1)
        self.assertEqual(len(self.store.audit(first["mission_id"])), 1)

    def test_idempotency_reuse_different_payload_denied(self):
        self.store.propose("home_browser_qa", self.home, "unique_01")
        with self.assertRaises(ValueError):
            self.store.propose("home_browser_qa", {**self.home, "home_path":"site/other.html"}, "unique_01")

    def test_idempotency_reject_injection(self):
        with self.assertRaises(ValueError):
            self.store.propose("home_browser_qa", self.home, "unsafe' DROP TABLE missions;")

    def test_id_lookup_reject_invalid(self):
        with self.assertRaises(ValueError):
            self.store.read("'; DROP TABLE missions; --")
        with self.assertRaises(KeyError):
            self.store.read("0" * 32)

    def test_persistent_between_instances(self):
        mission = self.store.propose("asset_integrity", {"filename":"reference.png"})
        other = MissionStore(self.tmp.name)
        self.assertEqual(other.read(mission["mission_id"]), mission)

    def test_no_op_without_state_dir(self):
        previous = os.environ.pop("MNIN_STATE_DIR", None)
        try:
            with self.assertRaises(RuntimeError):
                MissionStore()
        finally:
            if previous is not None:
                os.environ["MNIN_STATE_DIR"] = previous

    def test_audit_has_no_private_file_content(self):
        mission = self.store.propose("asset_integrity", {"filename": "logo.png"})
        db = Path(self.tmp.name) / "missions.sqlite3"
        self.assertTrue(db.exists())
        self.assertTrue(self.store.audit(mission["mission_id"]))
        self.assertEqual(self.store.read(mission["mission_id"])["inputs"]["filename"], "logo.png")


if __name__ == "__main__":
    unittest.main()
