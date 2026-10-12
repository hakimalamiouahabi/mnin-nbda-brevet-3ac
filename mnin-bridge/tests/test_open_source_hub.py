"""Tests for curated public OSS integration catalog and deterministic mission pipeline."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from open_source_hub import TOOLS, catalog_open_source_tools, open_source_pipeline


class OpenSourceHubTests(unittest.TestCase):
    def test_eight_upstreams_are_public_repository_urls(self):
        self.assertEqual(len(TOOLS), 8)
        ids = [entry["id"] for entry in TOOLS]
        self.assertEqual(len(ids), len(set(ids)))
        for item in TOOLS:
            self.assertTrue(item["url"].startswith("https://github.com/"))
            self.assertTrue(item["url"].endswith(item["repository"]))
            self.assertIn(item["license"], ("MIT", "Apache-2.0", "MPL-2.0"))
            self.assertTrue(item["package"])

    def test_catalog_is_not_misrepresented_as_native_chatgpt_install(self):
        info = catalog_open_source_tools()
        self.assertEqual(info["count"], 8)
        self.assertEqual(info["upstream_chatgpt_plugins_connected_by_this_catalog"], 0)
        self.assertEqual(info["remote_installations_performed"], 0)

    def test_domain_filter(self):
        tools = catalog_open_source_tools("accessibility")
        self.assertEqual({x["id"] for x in tools["upstreams"]},
                         {"axe_core", "html_validate"})
        self.assertEqual(catalog_open_source_tools("unmatched")["count"], 0)

    def test_reject_malformed_domains(self):
        for domain in ("*everything", "../secrets", "a" * 100, 9):
            with self.assertRaises(ValueError):
                catalog_open_source_tools(domain)

    def test_bounded_pipelines(self):
        for kind in ("home_qa", "asset_quality", "wordpress_development",
                     "bilingual_accessibility"):
            plan = open_source_pipeline(kind)
            self.assertEqual(plan["actual_execution"], "PLAN_ONLY")
            self.assertFalse(plan["requires_work_or_codex"])
            self.assertFalse(plan["site_writes_allowed"])
            self.assertTrue(all(x["test_result"] == "NON TESTÉ" and
                                not x["executed_now"] for x in plan["steps"]))
            self.assertEqual(
                [x["order"] for x in plan["steps"]],
                list(range(1, len(plan["steps"])+1)),
            )

    def test_unknown_pipeline_does_not_execute(self):
        with self.assertRaises(ValueError):
            open_source_pipeline("public_shell")


if __name__ == "__main__":
    unittest.main()
