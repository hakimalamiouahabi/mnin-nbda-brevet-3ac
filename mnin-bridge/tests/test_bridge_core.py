"""Run: python3 -m unittest discover -s mnin-bridge/tests -v"""
import hashlib
import os
import struct
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_core import asset_info, dispatch_qa, list_assets, validate_dispatch


class AssetTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        env = patch.dict(os.environ, {"MNIN_ASSET_ROOT": self.dir.name, "MNIN_ENABLE_DISPATCH": "0"})
        env.start()
        self.addCleanup(env.stop)
        self.data = (b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR"
                     + struct.pack(">II", 1024, 1536) + b"\x08\x06\x00\x00\x00" + b"test")
        (Path(self.dir.name) / "approved.png").write_bytes(self.data)

    def test_png_hash_and_dimensions(self):
        info = asset_info("approved.png", hashlib.sha256(self.data).hexdigest())
        self.assertTrue(info["matches_expected"])
        self.assertEqual(info["dimensions"], {"width": 1024, "height": 1536})
        self.assertEqual((Path(self.dir.name) / "approved.png").read_bytes(), self.data)

    def test_wrong_hash_is_not_accepted(self):
        self.assertFalse(asset_info("approved.png", "0" * 64)["matches_expected"])

    def test_invalid_expected_hash(self):
        with self.assertRaises(ValueError):
            asset_info("approved.png", "abc")

    def test_path_traversal_denied(self):
        for name in ("../approved.png", "secret/approved.png", "approved.png/.."):
            with self.assertRaises(ValueError):
                asset_info(name)

    def test_symlink_outside_denied(self):
        with tempfile.TemporaryDirectory() as external:
            target = Path(external) / "outside.png"
            target.write_bytes(self.data)
            link = Path(self.dir.name) / "link.png"
            try:
                link.symlink_to(target)
            except OSError:
                self.skipTest("Symlinks not supported")
            with self.assertRaises(ValueError):
                asset_info("link.png")

    def test_inventory_does_not_read_nonimages(self):
        (Path(self.dir.name) / "credentials.txt").write_text("secret")
        self.assertEqual(list_assets()["files"], ["approved.png"])


class DispatchTests(unittest.TestCase):
    def test_valid_branches(self):
        validate_dispatch("feature/home-v1", "site/index.html")

    def test_deny_untrusted_branches_and_urls(self):
        for branch, p in [
            ("main", "site/index.html"),
            ("feature/a", "../../etc/passwd"),
            ("feature/../../other", "site/index.html"),
            ("feature/a", "http://example.com/home.html"),
        ]:
            with self.assertRaises(ValueError):
                validate_dispatch(branch, p)

    def test_dispatch_disabled(self):
        with patch.dict(os.environ, {"MNIN_ENABLE_DISPATCH": "0"}):
            with self.assertRaises(RuntimeError):
                dispatch_qa("feature/home", "site/index.html", True)

    def test_dispatch_needs_explicit_approval(self):
        with patch.dict(os.environ, {"MNIN_ENABLE_DISPATCH": "1"}):
            with self.assertRaises(RuntimeError):
                dispatch_qa("feature/home", "site/index.html", False)


if __name__ == "__main__":
    unittest.main()
