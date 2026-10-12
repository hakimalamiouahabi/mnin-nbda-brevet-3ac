"""AssetLab structural tests. No internet, model API, storage upload or file mutation."""
import json
import os
import struct
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality_lab import inspect_asset


class AssetLabTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        env = patch.dict(os.environ, {"MNIN_ASSET_ROOT": self.tmp.name})
        env.start()
        self.addCleanup(env.stop)
        self.root = Path(self.tmp.name)
        self.png = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + struct.pack(">II", 1024, 1536)
        (self.root / "official.png").write_bytes(self.png)

    def test_png_native_dimensions_and_dpr(self):
        r = inspect_asset("official.png", 500, 2)
        self.assertEqual((r["intrinsic_width"],r["intrinsic_height"]),(1024,1536))
        self.assertTrue(r["density_pass"])
        self.assertTrue(r["does_not_claim_8k"])

    def test_png_low_density_flag(self):
        r = inspect_asset("official.png", 800, 3)
        self.assertEqual(r["min_intrinsic_width_for_density"], 2400)
        self.assertFalse(r["density_pass"])

    def test_png_corrupt_rejected(self):
        (self.root / "broken.png").write_bytes(b"not-png")
        with self.assertRaises(ValueError):
            inspect_asset("broken.png")

    def test_jpeg_sof_dimensions(self):
        sof = b"\xff\xd8" + b"\xff\xc0" + struct.pack(">H",8) + struct.pack(">BHHB",8,960,1280,3)
        (self.root/"sample.jpg").write_bytes(sof)
        r=inspect_asset("sample.jpg",640,2)
        self.assertEqual((r["intrinsic_width"],r["intrinsic_height"]),(1280,960))
        self.assertTrue(r["density_pass"])

    def test_webp_vp8x_dimensions(self):
        w,h=2300,1200
        header=(b"RIFF"+b"\x00"*4+b"WEBP"+b"VP8X"+b"\x0a\x00\x00\x00"+
                b"\x00"*4+(w-1).to_bytes(3,"little")+(h-1).to_bytes(3,"little"))
        (self.root/"sample.webp").write_bytes(header)
        r=inspect_asset("sample.webp",500,3)
        self.assertEqual((r["intrinsic_width"],r["intrinsic_height"]),(2300,1200))
        self.assertTrue(r["density_pass"])

    def test_svg_responsive_viewbox(self):
        (self.root/"icon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="14"/></svg>')
        r=inspect_asset("icon.svg")
        self.assertEqual(r["viewbox"],[0.,0.,32.,32.])
        self.assertEqual(r["embedded_images"],0)

    def test_svg_raster_embedded_warning(self):
        (self.root/"icon.svg").write_text('<svg viewBox="0 0 32 32"><image href="placeholder.png"/></svg>')
        r=inspect_asset("icon.svg")
        self.assertEqual(r["embedded_images"],1)

    def test_svg_doctype_entity_denied(self):
        (self.root/"evil.svg").write_text('<!DOCTYPE svg [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><svg viewBox="0 0 3 3">&xxe;</svg>')
        with self.assertRaises(ValueError):
            inspect_asset("evil.svg")

    def test_svg_missing_viewbox_denied(self):
        (self.root/"noview.svg").write_text('<svg width="40" height="40"></svg>')
        with self.assertRaises(ValueError):
            inspect_asset("noview.svg")

    def test_svg_script_identified(self):
        (self.root/"script.svg").write_text('<svg viewBox="0 0 3 3"><script>throw 1</script></svg>')
        self.assertEqual(inspect_asset("script.svg")["script_elements"],1)

    def test_glb_scene_and_animation_metadata(self):
        document={"asset":{"version":"2.0"},"scenes":[{"nodes":[0]}],
                  "nodes":[{"mesh":0}],"meshes":[{}],
                  "materials":[{}],"animations":[{}]}
        raw=json.dumps(document).encode()
        raw+=b" " * ((-len(raw)) % 4)
        total=20+len(raw)
        contents=struct.pack("<4sIIII",b"glTF",2,total,len(raw),0x4e4f534a)+raw
        (self.root/"amine.glb").write_bytes(contents)
        r=inspect_asset("amine.glb")
        self.assertEqual(r["animations"],1)
        self.assertEqual(r["scenes"],1)
        self.assertIn("not a render",r["quality_warning"])

    def test_glb_invalid_chunk_rejected(self):
        (self.root/"broken.glb").write_bytes(b"fake data")
        with self.assertRaises(ValueError):
            inspect_asset("broken.glb")

    def test_path_traversal_rejected(self):
        for file in ("../official.png", "other/official.png", "/tmp/sneaky.png"):
            with self.subTest(file=file):
                with self.assertRaises(ValueError):
                    inspect_asset(file)

    def test_svg_external_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as ext:
            outside=Path(ext)/"outside.svg"
            outside.write_text('<svg viewBox="0 0 2 2"/>')
            link=self.root/"link.svg"
            try:
                link.symlink_to(outside)
            except OSError:
                self.skipTest("symlink unavailable")
            with self.assertRaises(ValueError):
                inspect_asset("link.svg")

    def test_invalid_dpr_and_size_denied(self):
        for width,dpr in ((-1,2),(9000,2),(100,0),(100,5)):
            with self.subTest(width=width,dpr=dpr):
                with self.assertRaises(ValueError):
                    inspect_asset("official.png",width,dpr)

    def test_glb_not_image(self):
        with self.assertRaises(ValueError):
            inspect_asset("other.html")

if __name__=="__main__":
    unittest.main()
