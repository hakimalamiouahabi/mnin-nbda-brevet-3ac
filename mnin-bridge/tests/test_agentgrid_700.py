"""AgentGrid 700 integration tests. All execution is deterministic and offline."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agentgrid import AgentGrid, EXPECTED, MISSION_SPECS, roster_status


class AgentGridTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grid = AgentGrid()

    def test_exact_profiles_counts(self):
        s=roster_status()
        self.assertEqual(s["total_profiles"],700)
        self.assertEqual(s["counts"],EXPECTED)
        self.assertEqual(s["agents_running"],0)

    def test_five_divisions_of_140_each(self):
        items=self.grid.divisions()
        self.assertEqual(len(items),5)
        for d in items:
            self.assertEqual(d["profile_count"],140)
            self.assertEqual(d["senior_managers"],6)
            self.assertEqual(d["managers"],12)
            self.assertEqual(d["team_leaders"],12)
            self.assertEqual(d["experts"],109)

    def test_every_expert_reports_to_an_actual_dsi(self):
        dsi_ids={x["dsi"] for x in self.grid.divisions()}
        for p in self.grid.profiles:
            chain=self.grid.ancestors(p["id"])
            self.assertTrue(chain or p["level"]=="dsi")
            if chain:
                self.assertIn(chain[0]["id"],dsi_ids)
                self.assertLessEqual(len(chain),4)

    def test_all_mission_kinds_have_route(self):
        for kind in MISSION_SPECS:
            with self.subTest(kind=kind):
                result=self.grid.route(kind)
                self.assertEqual(result["mission_kind"],kind)
                self.assertEqual(result["scheduled_expert_slots"],9)
                self.assertEqual(result["execution_status"],"PLAN_ONLY")
                self.assertEqual(result["actually_spawned_ai_agents"],0)
                self.assertEqual(result["calls_to_paid_ai_apis"],0)
                self.assertEqual(result["write_operations_performed"],0)
                self.assertEqual(len(result["expert_ids"]),len(set(result["expert_ids"])))

    def test_role_chain_is_preserved_in_plan(self):
        result=self.grid.route("home_8k_asset_qa",12)
        given={p["id"] for p in result["roles"]}
        for role in result["roles"]:
            self.assertEqual(role["state"],"PLANNED_NOT_RUNNING")
            if role["reports_to"]!="OWNER":
                self.assertIn(role["reports_to"],given)

    def test_home_qa_relevant_divisions(self):
        r=self.grid.route("home_browser_qa",12)
        self.assertEqual(r["selected_dsi"],["DSI_01","DSI_02","DSI_05"])

    def test_cloudflare_audit_relevant_divisions(self):
        r=self.grid.route("cloudflare_d1_readonly_audit",12)
        self.assertEqual(r["selected_dsi"],["DSI_04","DSI_05","DSI_02"])

    def test_portfolio_is_throttled_not_executed(self):
        x=self.grid.portfolio(["home_8k_asset_qa","cloudflare_d1_readonly_audit","github_maintenance_review"],expert_limit=9,max_concurrent_jobs=2)
        self.assertEqual(x["portfolio_size"],3)
        self.assertEqual([len(z) for z in x["batches"]],[2,1])
        self.assertEqual(x["actual_agents_running"],0)
        self.assertEqual(x["actual_concurrent_jobs"],0)
        self.assertEqual(x["max_incremental_eur"],0)

    def test_find_vector_experts(self):
        result=self.grid.search("vector",limit=10)
        self.assertGreater(len(result),0)
        self.assertLessEqual(len(result),10)

    def test_profile_lookup_rejects_nonexistent(self):
        with self.assertRaises(ValueError):
            self.grid.ancestors("OWNER")
        with self.assertRaises(ValueError):
            self.grid.ancestors("EX_NOT_REAL")

    def test_reject_unknown_or_overbudget_missions(self):
        for name, cap in [("arbitrary-shell",10),("home_browser_qa",0),("home_browser_qa",16)]:
            with self.subTest(name=name, cap=cap):
                with self.assertRaises(ValueError):
                    self.grid.route(name,cap)

    def test_reject_unbounded_parallelism(self):
        with self.assertRaises(ValueError):
            self.grid.portfolio(["home_browser_qa"],max_concurrent_jobs=4)

    def test_reject_duplicate_or_unknown_portfolios(self):
        for kinds in [[],["home_browser_qa","home_browser_qa"],["secret_export"],["home_browser_qa"]*6]:
            with self.subTest(kinds=kinds):
                with self.assertRaises(ValueError):
                    self.grid.portfolio(kinds)

    def test_corrupted_manifest_rejected(self):
        original=json.loads((Path(__file__).resolve().parents[1]/"agentgrid"/"profiles-700.json").read_text())
        scenarios=[
            lambda d:d["profiles"].pop(),
            lambda d:d["profiles"][1].update(id=d["profiles"][0]["id"]),
            lambda d:d["profiles"][1].update(parent_id="MISSING_PARENT"),
            lambda d:d["profiles"][0].update(parent_id="MGR_1_01_1"),
        ]
        for corrupt in scenarios:
            with self.subTest(corrupt=str(corrupt)):
                payload=json.loads(json.dumps(original))
                corrupt(payload)
                with tempfile.TemporaryDirectory() as folder:
                    path=Path(folder)/"bad.json"
                    path.write_text(json.dumps(payload))
                    with self.assertRaises(ValueError):
                        AgentGrid(path)

    def test_no_bypass_through_user_defined_operations(self):
        for attack in ["wordpress.production_write","delete_cloudflare_database","deploy_all_700_agents"]:
            with self.assertRaises(ValueError):
                self.grid.route(attack)


if __name__=="__main__":
    unittest.main()
