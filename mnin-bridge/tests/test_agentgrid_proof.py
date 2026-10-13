"""Evidence tests for the original 700-role AgentGrid, no AI execution."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agentgrid_proof import build_report, grid_manifest_path

class AgentGridProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = build_report()

    def test_all_700_roles_are_counted(self):
        r = self.report
        self.assertEqual(r["existing_role_definitions"], 700)
        self.assertEqual(r["per_profile_structural_checks_executed"], 700)
        self.assertEqual(r["unique_ids"], 700)
        self.assertTrue(r["hierarchies_valid"])
        self.assertEqual(r["counts"], r["expected_counts"])

    def test_exact_five_dsi_and_no_new_roles(self):
        r = self.report
        self.assertEqual(len(r["dsi_coverage"]), 5)
        self.assertEqual(list(r["dsi_coverage"].values()), [140] * 5)
        self.assertEqual(len(r["per_profile_verifications"]), 700)

    def test_manifests_are_unchanged_by_plan(self):
        path = Path(grid_manifest_path())
        previous = path.read_bytes()
        build_report(["home_browser_qa"])
        self.assertEqual(path.read_bytes(), previous)

    def test_seven_valid_missions(self):
        self.assertEqual(len(self.report["mission_routes"]), 7)
        self.assertTrue(all(
            m["scheduled_expert_slots"] == 9 for m in self.report["mission_routes"]
        ))
        self.assertTrue(all(m["actually_spawned_ai_agents"] == 0 for m in self.report["mission_routes"]))

    def test_no_false_running_claims(self):
        r = self.report
        self.assertEqual(r["independent_ai_agent_sessions_started"], 0)
        self.assertEqual(r["ai_inference_calls"], 0)
        self.assertEqual(r["paid_ai_api_calls"], 0)
        self.assertEqual(r["wordpress_changes"], 0)
        self.assertEqual(r["cloudflare_writes"], 0)

    def test_per_profile_check_not_misrepresented_as_ai(self):
        self.assertTrue(all(
            c["hierarchy_verified"] and not c["ai_session_started"]
            for c in self.report["per_profile_verifications"]
        ))

    def test_duplicate_kinds_rejected(self):
        with self.assertRaises(ValueError):
            build_report(["home_browser_qa", "home_browser_qa"])

    def test_unknown_mission_kind_rejected(self):
        with self.assertRaises(ValueError):
            build_report(["delete_everything"])

    def test_evidence_json_serializable(self):
        doc = json.dumps(self.report)
        self.assertIn("manifest_sha256", doc)
        self.assertNotIn("token_secret",doc)

if __name__=="__main__":
    unittest.main()
