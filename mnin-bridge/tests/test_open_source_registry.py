"""OSS registry contract tests: no downloads, no remote code execution."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import open_source_registry as oss


class RegistryTests(unittest.TestCase):
    def test_eleven_repositories_are_registered(self):
        result=oss.list_upstreams()
        self.assertEqual(result["count"],11)
        self.assertFalse(result["actually_linked_to_chatgpt_pro"])
        self.assertTrue(all(p["url"].startswith("https://github.com/") for p in result["projects"]))

    def test_tools_are_not_falsely_reported_running(self):
        status=oss.readiness()
        self.assertEqual(status["registered_projects"],11)
        self.assertFalse(status["remote_mcp_endpoint_active"])
        self.assertFalse(status["github_repos_are_plugins"])
        self.assertTrue(status["runner_npm_dependency_manifest_present"])

    def test_domain_filter(self):
        projects=oss.list_upstreams("BrowserLab")["projects"]
        self.assertEqual([p["id"] for p in projects],["microsoft/playwright"])

    def test_invalid_filter_denied(self):
        with self.assertRaises(ValueError):
            oss.list_upstreams("../etc/passwd")

    def test_no_duplicate_repositories(self):
        ids=[p["id"] for p in oss.list_upstreams()["projects"]]
        self.assertEqual(len(ids),len(set(ids)))

    def test_reject_injected_host(self):
        source=oss.REGISTRY.read_text()
        data=json.loads(source)
        data["projects"][0]["url"]="https://evil.example.com/x"
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"registry.json"
            path.write_text(json.dumps(data))
            with patch.object(oss,"REGISTRY",path):
                with self.assertRaises(ValueError):
                    oss.list_upstreams()

    def test_reject_public_github_spoof(self):
        source=oss.REGISTRY.read_text()
        data=json.loads(source)
        data["projects"][0]["url"]="https://github.com.evil.invalid/microsoft/playwright"
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"registry.json"
            path.write_text(json.dumps(data))
            with patch.object(oss,"REGISTRY",path):
                with self.assertRaises(ValueError):
                    oss.list_upstreams()

    def test_reject_unsupported_license(self):
        data=json.loads(oss.REGISTRY.read_text())
        data["projects"][0]["license"]="unknown-private"
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"registry.json"
            path.write_text(json.dumps(data))
            with patch.object(oss,"REGISTRY",path):
                with self.assertRaises(ValueError):
                    oss.list_upstreams()

    def test_reject_duplicate(self):
        data=json.loads(oss.REGISTRY.read_text())
        data["projects"][1]["id"]=data["projects"][0]["id"]
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"registry.json"
            path.write_text(json.dumps(data))
            with patch.object(oss,"REGISTRY",path):
                with self.assertRaises(ValueError):
                    oss.list_upstreams()

if __name__=="__main__":
    unittest.main()
