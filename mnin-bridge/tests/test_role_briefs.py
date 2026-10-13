"""Test prompts/contracts of exactly the existing 700 roles, no autonomous models."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from role_briefs import role_brief, full_contract_inventory

class RoleContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inv=full_contract_inventory()

    def test_700_and_no_new_profiles(self):
        self.assertEqual(self.inv["total_existing_roles"],700)
        self.assertEqual(self.inv["additional_roles_created"],0)
        self.assertEqual(self.inv["individual_ai_agents_running"],0)
        self.assertEqual(len(self.inv["contracts"]),700)

    def test_all_contracts_unique_and_ready_for_manual_use(self):
        cs=self.inv["contracts"]
        self.assertEqual(len({c["role_id"] for c in cs}),700)
        self.assertTrue(all(c["professional_quality_gate"] for c in cs))
        self.assertTrue(all(c["instructions"] for c in cs))
        self.assertTrue(all(c["execution"]=="ROLE_BRIEF_ONLY" for c in cs))

    def test_contracts_are_not_mislabelled_as_started_agents(self):
        self.assertFalse(any(c["independent_ai_agent_running"] for c in self.inv["contracts"]))
        self.assertFalse(any(c["is_new_role"] for c in self.inv["contracts"]))

    def test_specific_existing_expert_and_chain(self):
        p=role_brief("EX_1_01_1_01","home_8k_asset_qa")
        self.assertEqual(p["level"],"expert")
        self.assertEqual(p["dsi_id"],"DSI_01")
        self.assertEqual(len(p["management_chain"]),4)
        self.assertEqual(p["mission_kind"],"home_8k_asset_qa")
        self.assertTrue(p["mission_goal"])

    def test_only_existing_professional_identifiers_allowed(self):
        with self.assertRaises(ValueError):
            role_brief("NEW_800th_AGENT")
        with self.assertRaises(ValueError):
            role_brief("../.env")

    def test_unknown_mission_denied(self):
        with self.assertRaises(ValueError):
            role_brief("DSI_01","cloudflare_delete_all")

    def test_not_exfiltrating_credentials(self):
        js=json.dumps(self.inv)
        self.assertNotIn("MNIN_GITHUB_TOKEN",js)
        self.assertNotIn("MNIN_OWNER_SUB",js)

if __name__=="__main__":
    unittest.main()
