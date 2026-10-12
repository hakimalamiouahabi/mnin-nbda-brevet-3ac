"""Read-only MNIN premium suite tests. No WordPress, GitHub API or paid API calls."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from premium_suite import MODULES, delegation_status, module_catalog, propose_premium_plan


class PremiumSuiteTests(unittest.TestCase):
    def test_ten_modules(self):
        catalog = module_catalog()
        self.assertEqual(catalog["module_count"], 10)
        self.assertEqual(len(catalog["modules"]), 10)
        self.assertEqual(catalog["agents_actually_started"], 0)
        self.assertEqual(catalog["execution"], "PLAN_ONLY")

    def test_intent_routes_supported_modules(self):
        plan = propose_premium_plan("Auditer la Home WordPress responsive RTL et les images 8K")
        self.assertIn("wordpress_core", plan["selected_modules"])
        self.assertIn("responsive_fr_ar", plan["selected_modules"])
        self.assertIn("assets_hd", plan["selected_modules"])
        self.assertEqual(plan["effect"], "NO REMOTE ACTION PERFORMED")

    def test_explicit_modules_have_stable_order(self):
        chosen = ["qualite_livraison", "direction_artistique"]
        plan = propose_premium_plan("Créer une présentation premium", chosen)
        self.assertEqual(plan["selected_modules"], ["direction_artistique", "qualite_livraison"])
        self.assertTrue(all(step["roles_spawned"] == 0 for step in plan["steps"]))

    def test_fallback_is_bounded(self):
        plan = propose_premium_plan("Étudier la demande")
        self.assertEqual(plan["selected_modules"],
                         ["direction_artistique", "wordpress_core", "qualite_livraison"])

    def test_invalid_inputs(self):
        for task, selected in [("", None), ("a", None), ("bien", ["intrusion"]),
                               ("bien", ["wordpress_core", 123]),
                               ("bien", list(MODULES) + ["wordpress_core"])]:
            with self.subTest(task=task, selected=selected):
                with self.assertRaises(ValueError):
                    propose_premium_plan(task, selected)

    def test_consents_do_not_grant_runtime_access(self):
        info = delegation_status("dev.branch_write")
        self.assertEqual(info["classification"], "STANDING_INSTRUCTION")
        self.assertTrue(info["owner_standing_instruction"])
        self.assertFalse(info["runtime_execution_authorized"])
        self.assertFalse(info["chatgpt_pro_entitlement_verified"])
        self.assertEqual(info["policy_status"], "TEMPLATE_NOT_ACTIVATED")

    def test_mutations_need_distinct_approval(self):
        for action in ("wordpress.production_write", "github.merge_to_main",
                       "billing.charge", "mass_delete"):
            self.assertEqual(delegation_status(action)["classification"],
                             "EXPLICIT_PER_ACTION_APPROVAL")

    def test_critical_actions_are_not_authorized(self):
        for action in ("secrets.export", "child_data.export",
                       "unrestricted_shell", "unbounded_agent_execution"):
            info = delegation_status(action)
            self.assertEqual(info["classification"], "BLOCK_WITHOUT_SEPARATE_CAPABILITY")
            self.assertFalse(info["runtime_execution_authorized"])

    def test_unknown_actions_are_refused(self):
        self.assertEqual(delegation_status("arbitrary.sudo")["classification"], "NOT_ALLOWED")
        with self.assertRaises(ValueError):
            delegation_status("x" * 200)


if __name__ == "__main__":
    unittest.main()
