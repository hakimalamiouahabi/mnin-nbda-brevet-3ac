"""700-profile registry must never be presented as 700 running AI agents."""
from __future__ import annotations
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agents_700 import _registry, registry_700_status, search_agent_700, plan_700_mission

class Registry700Tests(unittest.TestCase):
    def test_every_profile_and_hierarchy_is_valid(self):
        source, profiles = _registry()
        self.assertEqual(len(profiles), 700)
        self.assertEqual(source["status"], "TARGET_NOT_DEPLOYED")
        self.assertEqual(
            {key: len([v for v in profiles.values() if v["level"] == key])
             for key in ("dsi", "senior_manager", "manager", "team_leader", "expert")},
            {"dsi": 5, "senior_manager": 30, "manager": 60,
             "team_leader": 60, "expert": 545},
        )

    def test_status_covers_all_545_experts(self):
        result = registry_700_status()
        self.assertEqual(result["documented_profiles"], 700)
        self.assertEqual(result["experts_assigned_to_modules"], 545)
        self.assertEqual(sum(result["expert_coverage_by_module"].values()), 545)
        self.assertEqual(result["specialist_groups"], 30)
        self.assertEqual(len(result["directorate_profiles"]), 5)
        self.assertEqual(result["running_autonomous_agents_verified"], 0)
        self.assertEqual(result["runtime"], "PROFILE_REGISTRY_ONLY")

    def test_search_experts_with_reporting_chain(self):
        r = search_agent_700("architecture WordPress PHP", "wordpress_core")
        self.assertGreater(r["total_matched"], 0)
        self.assertLessEqual(len(r["profiles"]), 8)
        for item in r["profiles"]:
            self.assertEqual(item["responsibility_chain"][0]["id"], "OWNER")
            self.assertEqual(item["responsibility_chain"][1]["level"], "dsi")
            self.assertEqual(item["responsibility_chain"][-1]["id"], item["id"])
            self.assertEqual(item["module"], "wordpress_core")
            self.assertEqual(item["execution_state"], "CATALOGUED_NOT_RUNNING")
            self.assertEqual(item["actions_performed"], 0)

    def test_no_false_700_agent_parallel_execution(self):
        r = plan_700_mission("Vérifier le site marocain et son accessibilité",
                             ["wordpress_core", "accessibilite", "qualite_livraison"])
        self.assertEqual(r["profiles_catalogued"], 700)
        self.assertEqual(r["running_agents_verified"], 0)
        self.assertEqual(r["execution"], "BLUEPRINT_NOT_STARTED")
        self.assertEqual(r["paid_ai_api_calls"], 0)
        self.assertFalse(r["requires_work_or_codex"])
        self.assertEqual(len(r["steps"]), 3)
        self.assertEqual([s["depends_on"] for s in r["steps"]],
                         [None, "wordpress_core", "accessibilite"])
        self.assertTrue(all(s["execution_status"] == "NON TESTÉ" for s in r["steps"]))

    def test_search_input_bounds(self):
        for text, mod, cap in (
            ("", "", 8), ("a", "", 8), ("OK", "", 8),
            ("audit WordPress", "bad_module", 8),
            ("audit WordPress", "", 0), ("audit WordPress", "", 21),
            ("audit WordPress", "", True),
        ):
            with self.subTest(text=text, module=mod, cap=cap):
                with self.assertRaises(ValueError):
                    search_agent_700(text, mod, cap)

    def test_plan_input_bounds(self):
        for mod in (
            [], ["bad_module"], ["wordpress_core", "wordpress_core"],
            ["wordpress_core"] * 11,
        ):
            with self.subTest(mod=mod):
                with self.assertRaises(ValueError):
                    plan_700_mission("Créer un projet éducatif", mod)

    def test_duplicate_manifest_rejected(self):
        source, _ = _registry()
        source["profiles"][1]["id"] = source["profiles"][0]["id"]
        self._refuse(source)

    def test_rogue_parent_rejected(self):
        source, _ = _registry()
        source["profiles"][-1]["parent_id"] = "unknown"
        self._refuse(source)

    def test_fake_running_agent_rejected(self):
        source, _ = _registry()
        expert = next(o for o in source["profiles"] if o["level"] == "expert")
        expert["state"] = "running"
        self._refuse(source)

    def test_incomplete_group_rejected(self):
        source, _ = _registry()
        for profile in source["profiles"]:
            if profile.get("competency_group") == "Direction artistique, marque et design premium":
                profile["competency_group"] = "no-such-specialty"
                break
        self._refuse(source)

    def _refuse(self, source):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "broken.json"
            p.write_text(json.dumps(source), encoding="utf-8")
            with self.assertRaises(ValueError):
                _registry(p)

if __name__ == "__main__":
    unittest.main()
