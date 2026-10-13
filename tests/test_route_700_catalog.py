#!/usr/bin/env python3
"""Tests automatiques sans connexion à WordPress, Cloudflare ou à une API d'IA."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("route_700_catalog", ROOT / "scripts" / "route_700_catalog.py")
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)
CATALOG = json.loads((ROOT / "agents" / "manifest-700-target.json").read_text(encoding="utf-8"))
IDS = {p["id"] for p in CATALOG["profiles"]}

class TestRoutage(unittest.TestCase):
    def test_registre_inchange(self):
        self.assertEqual(len(CATALOG["profiles"]), 700)
        self.assertEqual(len(IDS), 700)
        self.assertEqual(CATALOG["status"], "TARGET_NOT_DEPLOYED")

    def check_mission(self, sentence):
        result = router.route(CATALOG, sentence, count=6)
        self.assertEqual(result["status"], "ROUTAGE_PRET", sentence)
        self.assertTrue(result["no_new_agents"])
        self.assertFalse(result["inference_started"])
        self.assertGreaterEqual(result["selected"], 2)
        titles = [item["title"] for item in result["assignments"]]
        self.assertEqual(len(titles), len(set(titles)))
        for item in result["assignments"]:
            self.assertIn(item["id"], IDS)
            self.assertEqual(item["chain"][-1]["id"], item["id"])
            self.assertEqual(len(item["chain"]), 5)
        return titles

    def test_panne_generique(self):
        titles = self.check_mission("Mon outil Équipe 700 ne fonctionne plus")
        self.assertIn("Expert incident response", titles)

    def test_cloudflare_wordpress(self):
        titles = self.check_mission("Optimise mes bases Cloudflare et mon site WordPress")
        self.assertIn("Architecte WordPress", titles)
        self.assertIn("Ingénieur base de données", titles)

    def test_application_educative(self):
        titles = self.check_mission("Développe une application éducative")
        self.assertIn("Ingénieur pédagogique", titles)

    def test_sans_expert_direct(self):
        result = router.route(CATALOG, "Trouve des subventions publiques françaises")
        self.assertEqual(result["status"], "AUCUN_PROFIL_IDENTIFIE")
        self.assertEqual(result["assignments"], [])

    def test_identifiant_exact(self):
        result = router.route(CATALOG, "Vérifie le site", role_id="EX_2_01_1_01")
        self.assertEqual([x["id"] for x in result["assignments"]], ["EX_2_01_1_01"])

    def test_identifiant_invente_interdit(self):
        with self.assertRaises(ValueError):
            router.route(CATALOG, "Vérifie le site", role_id="EX_FAUX_123")

if __name__ == "__main__":
    unittest.main()
