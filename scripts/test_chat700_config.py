"""Guardrails for one-ChatGPT-conversation coordination of the original 700 roles."""
import json
import unittest
from pathlib import Path
from scripts.route_700_catalog import route

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "chat700_operating_mode.json"
MANIFEST = ROOT / "agents" / "manifest-700-target.json"
DOC = ROOT / "docs" / "CHATGPT_700_PROJET_INSTRUCTIONS.md"


class Chat700ModeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = json.loads(CONFIG.read_text(encoding="utf-8"))
        cls.m = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_only_original_700_profiles(self):
        self.assertEqual(len(self.m["profiles"]), 700)
        self.assertEqual(self.c["manifest"]["expected_count"], 700)
        self.assertEqual(self.c["manifest"]["expected_levels"], self.m["counts"])
        self.assertTrue(self.c["manifest"]["write_protected"])
        self.assertFalse(self.c["manifest"]["allow_new_roles"])
        self.assertEqual(len({p["id"] for p in self.m["profiles"]}), 700)
        self.assertEqual(self.m["status"], "TARGET_NOT_DEPLOYED")

    def test_only_chatgpt_no_paid_ai_or_other_surface(self):
        channel = self.c["channel"]
        self.assertEqual(channel["mode"], "standard_chat_only")
        self.assertFalse(channel["requires_work"])
        self.assertFalse(channel["requires_codex"])
        self.assertEqual(channel["model_api_cost_eur"], 0)
        self.assertFalse(channel["extra_server_required"])
        self.assertFalse(self.c["safety"]["no_work_or_codex"] is False)
        self.assertTrue(self.c["safety"]["no_paid_ai_apis"])

    def test_never_claim_700_independent_running_models(self):
        self.assertEqual(self.c["reasoning"]["independent_running_ai_agents"], 0)
        self.assertEqual(self.c["reasoning"]["engine"],
                         "CURRENT_CHATGPT_CONVERSATION_SINGLE_MODEL")
        self.assertFalse(self.c["reasoning"]["can_impersonate_many_independent_models"])
        self.assertEqual(self.c["execution_truth"]["agent_models_deployed"], 0)
        self.assertFalse(self.c["execution_truth"]["installed_native_plugin_by_this_file"])
        self.assertEqual(self.c["config_status"], "REPO_CONFIGURED_NOT_NATIVE_CONNECTED")

    def test_boundaries_protect_user_services(self):
        for name in ("no_wordpress_write_without_explicit_approval",
                     "no_cloudflare_mutation_without_explicit_approval",
                     "no_private_data_in_public_repo",
                     "no_merge_to_main_without_explicit_approval",
                     "no_automatic_cleanup_or_mass_deletion"):
            self.assertTrue(self.c["safety"][name])

    def test_can_assign_existing_experts_without_instances(self):
        count = self.c["task_assignment"]["default_specialist_count"]
        res = route(self.m, "Mon outil ne fonctionne plus, vérifie WordPress et Cloudflare", count)
        self.assertEqual(res["selected"], count)
        self.assertEqual(res["source_profiles"], 700)
        self.assertEqual(res["autonomous_agents_started"], 0)
        original = {p["id"] for p in self.m["profiles"]}
        self.assertTrue(all(p["id"] in original for p in res["assignments"]))
        self.assertTrue(all(p["chain"][0]["id"].startswith("DSI_")
                            for p in res["assignments"]))

    def test_project_instructions_not_global_runtime_installer(self):
        doc = DOC.read_text(encoding="utf-8")
        self.assertIn("La mention « Équipe 700 » est facultative", doc)
        self.assertIn("config/chat700_operating_mode.json", doc)
        self.assertFalse(self.c["channel"]["auto_enable_all_chats"])
        self.assertFalse(self.c["execution_truth"]["chatgpt_project_instructions_applied_by_this_file"])


if __name__ == "__main__":
    unittest.main()
