"""Check real role assignments and read-only ChatGPT Pro enterprise planning."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent_conductor import (
    WORKFLOWS, workforce_status, plan_enterprise_mission,
    subscription_gate_readiness,
)


class ConductorTests(unittest.TestCase):
    def test_actual_workforce_manifest(self):
        info = workforce_status()
        self.assertEqual(info["documented_roles"], 43)
        self.assertEqual(info["by_level"], {
            "director": 1,
            "senior_manager": 3,
            "manager": 3,
            "team_leader": 6,
            "agent": 30,
        })
        self.assertEqual(info["separate_running_agents_verified"], 0)

    def test_each_workflow_has_real_governance_chain(self):
        for name in WORKFLOWS:
            with self.subTest(workflow=name):
                plan = plan_enterprise_mission(name, "Réaliser une mission de qualité MNIN NBDA")
                self.assertEqual(len(plan["all_stages"]), len(WORKFLOWS[name]))
                self.assertEqual(plan["execution_mode"], "BLUEPRINT_ONLY")
                for i, step in enumerate(plan["all_stages"]):
                    chain = step["responsibility"]
                    self.assertEqual(chain[0]["id"], "DSI")
                    self.assertEqual(chain[-1]["id"], step["specialist"])
                    self.assertEqual(
                        [role["level"] for role in chain],
                        ["director", "senior_manager", "manager", "team_leader", "agent"],
                    )
                    self.assertEqual(step["state"], "NON TESTÉ")
                    self.assertFalse(step["executed"])
                    self.assertEqual(step["evidence_collected"], [])
                    self.assertEqual(step["depends_on"],
                                     plan["all_stages"][i-1]["step_id"] if i else None)

    def test_invalid_task_does_not_produce_plan(self):
        for name, objective in (
            ("arbitrary_shell", "Run dangerous commands now"),
            ("premium_home", ""),
            ("premium_home", "ok"),
            ("premium_home", "a" * 2501),
        ):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    plan_enterprise_mission(name, objective)

    def test_no_unverified_pro_entitlement_granted(self):
        status = subscription_gate_readiness()
        self.assertFalse(status["strict_pro_only_server_gate_ready"])
        self.assertFalse(status["privileged_custom_mcp_writes_enabled"])
        self.assertEqual(status["conclusion"], "BLOQUÉ")
        self.assertEqual(status["excluded_surfaces"], ["Work", "Codex"])

    def test_missing_manifest_fails_closed(self):
        with self.assertRaises(FileNotFoundError):
            plan_enterprise_mission(
                "premium_home", "Auditer la Home MNIN NBDA", Path("/unavailable/manifest.json")
            )


if __name__ == "__main__":
    unittest.main()
