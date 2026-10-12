"""Tests for offline HTML diagnostics: no paid APIs, live sites or network."""
import hashlib
import os
import struct
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from site_auditor import _dimensions, audit_local_home


class LocalSiteQATests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "site" / "images").mkdir(parents=True)
        env = patch.dict(os.environ, {"MNIN_SITE_ROOT": str(self.root)})
        env.start()
        self.addCleanup(env.stop)
        self.png_bytes = (
            b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR"
            + struct.pack(">II", 400, 300) + b"\x08\x06\x00\x00\x00"
        )
        (self.root / "site" / "images" / "logo.png").write_bytes(self.png_bytes)

    def _html(self, body, lang="fr", direction="ltr"):
        return (
            f'<html lang="{lang}" dir="{direction}"><head><title>MNIN NBDA</title>'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<meta name="description" content="Formation"></head>'
            f'<body><h1>Apprendre</h1>{body}</body></html>'
        )

    def _write(self, content):
        path = self.root / "site" / "index.html"
        path.write_text(content, encoding="utf-8")
        return path

    def test_good_local_raster_has_sha_dimensions_and_no_errors(self):
        path = self._write(self._html(
            '<img src="images/logo.png" alt="Logo MNIN" width="200" height="150">'
        ))
        original = path.read_bytes()
        report = audit_local_home("site/index.html")
        self.assertEqual(report["summary"]["errors"], 0)
        self.assertEqual(report["summary"]["warnings"], 0)
        self.assertEqual(report["images"][0]["asset_status"], "LOCAL")
        self.assertEqual(report["images"][0]["native_pixels"], {"width": 400, "height": 300})
        self.assertEqual(report["images"][0]["sha256"], hashlib.sha256(self.png_bytes).hexdigest())
        self.assertEqual(report["page_sha256"], hashlib.sha256(original).hexdigest())
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(report["execution"], "NO_NETWORK_NO_WORDPRESS_WRITES")

    def test_detect_broken_images_duplicate_ids_and_fragments(self):
        self._write(self._html(
            '<div id="duplicate"></div><div id="duplicate"></div>'
            '<a href="#unknown">Lire</a><img src="images/missing.png" width="120" height="50">'
        ))
        report = audit_local_home("site/index.html")
        codes = {x["code"] for x in report["issues"]}
        self.assertTrue({"IMG_ALT_MISSING", "BROKEN_LOCAL_IMAGE", "DUPLICATE_ID",
                         "BROKEN_FRAGMENT"} <= codes)
        self.assertEqual(report["summary"]["errors"], 1)

    def test_low_resolution_png_warning(self):
        self._write(self._html(
            '<img src="images/logo.png" alt="" width="300" height="200">'
        ))
        codes = {x["code"] for x in audit_local_home("site/index.html", target_dpr=2)["issues"]}
        self.assertIn("RASTER_DPR_WARNING", codes)

    def test_arabic_must_declare_rtl(self):
        self._write(self._html("<p>مرحبا</p>", lang="ar", direction="ltr"))
        codes = {x["code"] for x in audit_local_home("site/index.html")["issues"]}
        self.assertIn("RTL_NOT_DECLARED", codes)

    def test_arabic_rtl_has_no_warning(self):
        self._write(self._html("<p>مرحبا</p>", lang="ar", direction="rtl"))
        self.assertEqual(audit_local_home("site/index.html")["summary"]["warnings"], 0)

    def test_no_network_fetch_of_external_images(self):
        self._write(self._html(
            '<img src="https://example.org/remote.png" alt="remote" width="100" height="100">'
        ))
        result = audit_local_home("site/index.html")
        self.assertEqual(result["images"][0]["asset_status"], "EXTERNAL_UNVERIFIED")

    def test_invalid_traversal_path_rejected(self):
        self._write(self._html("<p>ready</p>"))
        for item in ("../site/index.html", "site/../../secret.html",
                     "site/../index.html", "/site/index.html", "other/index.html",
                     "site/index.php", "site\\index.html"):
            with self.subTest(item=item), self.assertRaises(ValueError):
                audit_local_home(item)

    def test_malformed_attrs_do_not_crash(self):
        self._write("<html lang><head><title>X</title><meta name></head>"
                    "<body><h1>A</h1><img src width height><a href>go</a></body></html>")
        report = audit_local_home("site/index.html")
        self.assertEqual(report["images"][0]["asset_status"], "INVALID")

    def test_file_size_limit(self):
        self._write("A" * (2 * 1024 * 1024 + 1))
        with self.assertRaises(ValueError):
            audit_local_home("site/index.html")

    def test_invalid_dpr_is_refused(self):
        self._write(self._html("<p>Hello</p>"))
        for value in (0, 4, True, 1.5, "2"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                audit_local_home("site/index.html", value)

    def test_jpeg_width_height_order(self):
        jpeg = (b"\xff\xd8\xff\xc0\x00\x0b\x08"
                b"\x01\x90\x01\x2c\x03\x01\x11\x00\xff\xd9")
        f = self.root / "site" / "images" / "portrait.jpg"
        f.write_bytes(jpeg)
        self.assertEqual(_dimensions(f), (300, 400))

    def test_svg_is_identified_as_vector_not_8k(self):
        image = self.root / "site" / "images" / "brand.svg"
        image.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
        self._write(self._html('<img src="images/brand.svg" alt="logo" width="400" height="50">'))
        result = audit_local_home("site/index.html")
        self.assertTrue(result["images"][0]["vector"])
        self.assertNotIn("native_pixels", result["images"][0])

    def test_symlink_external_asset_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / "secret.png"
            external.write_bytes(self.png_bytes)
            link = self.root / "site" / "images" / "escape.png"
            try:
                link.symlink_to(external)
            except OSError:
                self.skipTest("Symbolic links unavailable")
            self._write(self._html(
                '<img src="images/escape.png" alt="escape" width="200" height="50">'
            ))
            report = audit_local_home("site/index.html")
            self.assertEqual(report["images"][0]["asset_status"], "REJECTED_OUT_OF_SCOPE")

    def test_no_private_root_configuration(self):
        self._write(self._html("<p>Hello</p>"))
        with patch.dict(os.environ, {"MNIN_SITE_ROOT": ""}):
            with self.assertRaises(RuntimeError):
                audit_local_home("site/index.html")


if __name__ == "__main__":
    unittest.main()
