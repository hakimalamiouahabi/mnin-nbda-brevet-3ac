"""Offline regression tests: routing uses original 700 roles, never AI inference."""
import copy
import json
import unittest
from pathlib import Path
from scripts.route_700_catalog import route

MANIFEST = Path(__file__).resolve().parents[1] / "agents" / "manifest-700-target.json"


class Chat700RoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.known = {p["id"]: p for p in cls.catalog["profiles"]}

    def assert_existing_chain(self, result):
        self.assertTrue(result["no_new_agents"])
        self.assertFalse(result["inference_started"])
        self.assertEqual(result["autonomous_agents_started"], 0)
        self.assertEqual(result["source_profiles"], 700)
        self.assertLessEqual(result["selected"], 30)
        for p in result["assignments"]:
            self.assertIn(p["id"], self.known)
            self.assertEqual(p["title"], self.known[p["id"]]["title"])
            self.assertEqual(p["chain"][-1]["id"], p["id"])
            self.assertEqual(p["chain"][0]["id"][:4], "DSI_")
            self.assertEqual(p["status"], "ROLE_ASSIGNE_NON_EXECUTE")

    def test_plain_french_broken_tool(self):
        r = route(self.catalog, "Équipe 700 : ton outil ne fonctionne plus", 5)
        self.assertGreater(r["selected"], 0)
        self.assertEqual(r["status"], "ROUTAGE_PRET")
        self.assert_existing_chain(r)
        self.assertTrue(any("QA logiciel" in p["competency_group"] for p in r["assignments"]))

    def test_plain_wordpress_home(self):
        r = route(self.catalog, "Corrige les bugs de ma page d'accueil WordPress", 7)
        self.assertGreaterEqual(r["selected"], 3)
        self.assert_existing_chain(r)
        self.assertTrue(any("WordPress" in p["competency_group"] for p in r["assignments"]))

    def test_cloudflare_d1(self):
        r = route(self.catalog, "Vérifie ma BDD Cloudflare D1 sans rien supprimer", 6)
        self.assertGreater(r["selected"], 0)
        self.assert_existing_chain(r)
        self.assertTrue(any("données" in p["competency_group"] or "Data engineering" in p["competency_group"]
                            for p in r["assignments"]))

    def test_design_and_bilingual(self):
        r = route(self.catalog, "Améliore le design responsive français arabe RTL", 6)
        self.assertGreater(r["selected"], 0)
        self.assert_existing_chain(r)

    def test_explicit_original_role(self):
        r = route(self.catalog, "Consulte ce profil", role_id="EX_2_01_1_01")
        self.assertEqual([x["id"] for x in r["assignments"]], ["EX_2_01_1_01"])
        self.assert_existing_chain(r)

    def test_uncovered_topic_reports_no_match(self):
        r = route(self.catalog, "zzzxyztown abcqqqunique", 5)
        self.assertEqual(r["status"], "AUCUN_PROFIL_IDENTIFIE")
        self.assertEqual(r["selected"], 0)

    def test_different_competencies_when_available(self):
        r = route(self.catalog, "WordPress bugs sécurité performance QA", 6)
        groups = [x["competency_group"] for x in r["assignments"]]
        self.assertEqual(len(groups), len(set(groups)))
        self.assert_existing_chain(r)

    def test_illegal_counts_and_nonexistent_agent(self):
        for count in (0, -1, 31, True, 2.5):
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    route(self.catalog, "Tester WordPress", count)
        with self.assertRaises(ValueError):
            route(self.catalog, "Tester", role_id="FAUX_001")

    def test_modified_manifest_is_rejected(self):
        for mutation in (
            lambda d: d["profiles"].pop(),
            lambda d: d["profiles"][1].update(id=d["profiles"][0]["id"]),
            lambda d: d["profiles"][1].update(parent_id="FOREIGN"),
            lambda d: d.update(status="DEPLOYED"),
            lambda d: next(p for p in d["profiles"] if p["level"] == "expert").update(state="running"),
        ):
            with self.subTest(mutation=repr(mutation)):
                data = copy.deepcopy(self.catalog)
                mutation(data)
                with self.assertRaises(ValueError):
                    route(data, "Vérifie WordPress")

    def test_no_mission_is_rejected(self):
        for mission in ("", "Équipe", "a", "de et"):
            with self.subTest(mission=mission):
                with self.assertRaises(ValueError):
                    route(self.catalog, mission)


if __name__ == "__main__":
    unittest.main()
