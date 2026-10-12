"""MNIN AssetLab v0.4 — inspect local original image/vector/GLB metadata.

No generation, network requests, shell execution, model calls or asset rewriting.
Never claim that upscaling makes an asset pixel-perfect. For real artwork, keep
the official original SHA-256 separate from production output files.
"""
from __future__ import annotations

import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

from bridge_core import _allowed_asset, asset_root, NAME


def _size(path: Path, limit: int = 100 * 1024 * 1024) -> int:
    sz = path.stat().st_size
    if sz <= 0 or sz > limit:
        raise ValueError("Asset size out of permitted range")
    return sz


def _jpeg_dimensions(path: Path) -> tuple[int, int]:
    """Parse dimensions from SOF marker, bounded streaming reads."""
    with path.open("rb") as f:
        if f.read(2) != b"\xff\xd8":
            raise ValueError("Not a JPEG")
        while True:
            if f.read(1) != b"\xff":
                raise ValueError("Malformed JPEG marker")
            marker = f.read(1)
            if not marker:
                raise ValueError("Truncated JPEG")
            while marker == b"\xff":
                marker = f.read(1)
            if marker in (b"\xd8", b"\x01"):
                continue
            if marker in (b"\xd9", b"\xda"):
                raise ValueError("JPEG has no readable SOF marker")
            n = f.read(2)
            if len(n) != 2:
                raise ValueError("Truncated JPEG marker segment")
            segment_len = struct.unpack(">H", n)[0]
            if segment_len < 2:
                raise ValueError("Invalid JPEG segment length")
            m = marker[0]
            if m in {0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf}:
                vals = f.read(5)
                if len(vals) != 5:
                    raise ValueError("Truncated JPEG SOF")
                _, h, w = struct.unpack(">BHH", vals)
                return w, h
            f.seek(segment_len - 2, 1)


def _png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        header = f.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("Invalid PNG header")
    return struct.unpack(">II", header[16:24])


def _webp_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        header = f.read(30)
    if len(header) < 30 or header[:4] != b"RIFF" or header[8:12] != b"WEBP":
        raise ValueError("Invalid WebP header")
    flavor = header[12:16]
    if flavor == b"VP8X":
        return 1 + int.from_bytes(header[24:27], "little"), 1 + int.from_bytes(header[27:30], "little")
    if flavor == b"VP8 " and header[23:26] == b"\x9d\x01\x2a":
        return struct.unpack("<H", header[26:28])[0] & 0x3fff, struct.unpack("<H", header[28:30])[0] & 0x3fff
    if flavor == b"VP8L" and header[20] == 0x2f:
        bits = int.from_bytes(header[21:25], "little")
        return (bits & 0x3fff) + 1, ((bits >> 14) & 0x3fff) + 1
    raise ValueError("Unsupported or malformed WebP header")


def _read_svg(path: Path) -> dict:
    _size(path, 15 * 1024 * 1024)
    raw = path.read_bytes()
    if re.search(rb"<!\s*(?:DOCTYPE|ENTITY)\b", raw, flags=re.I):
        raise ValueError("SVG DTD and entities are not permitted")
    root = ET.fromstring(raw)
    if not root.tag.endswith("}svg") and root.tag != "svg":
        raise ValueError("Not an SVG")
    viewbox = root.attrib.get("viewBox")
    if not viewbox:
        raise ValueError("SVG must contain viewBox for responsive use")
    vals = viewbox.replace(",", " ").split()
    if len(vals) != 4:
        raise ValueError("Invalid viewBox")
    try:
        coords = [float(n) for n in vals]
    except ValueError as exc:
        raise ValueError("Invalid viewBox coordinates") from exc
    if not (0 < coords[2] <= 50000 and 0 < coords[3] <= 50000):
        raise ValueError("Invalid viewBox size")
    elements = list(root.iter())
    if len(elements) > 20000:
        raise ValueError("SVG exceeds element-count safety budget")
    imgs = [e for e in elements if e.tag.endswith("}image") or e.tag == "image"]
    foreign = [e for e in elements if e.tag.endswith("}foreignObject") or e.tag == "foreignObject"]
    scripts = [e for e in elements if e.tag.endswith("}script") or e.tag == "script"]
    return {"type": "svg", "viewbox": coords, "elements": len(elements),
            "embedded_images": len(imgs), "foreign_objects": len(foreign),
            "script_elements": len(scripts),
            "quality_warning": "Vector is resolution-independent, but SVG content needs sanitization before web embedding"}


def _glb(path: Path) -> dict:
    sz = _size(path)
    with path.open("rb") as f:
        head = f.read(20)
        if len(head) != 20:
            raise ValueError("Truncated GLB")
        magic, version, total, chunk_length, chunk_type = struct.unpack("<4sIIII", head)
        if magic != b"glTF" or version != 2 or total != sz:
            raise ValueError("Not a valid GLB v2 header")
        if chunk_type != 0x4e4f534a or chunk_length > min(sz - 20, 25 * 1024 * 1024):
            raise ValueError("Invalid GLB JSON chunk")
        data = f.read(chunk_length)
    doc = json.loads(data.rstrip(b" \t\r\n\x00").decode("utf-8"))
    if doc.get("asset", {}).get("version") != "2.0":
        raise ValueError("GLB JSON missing glTF 2.0 asset declaration")
    return {"type": "glb", "bytes": sz,
            "scenes": len(doc.get("scenes", [])),
            "meshes": len(doc.get("meshes", [])),
            "materials": len(doc.get("materials", [])),
            "textures": len(doc.get("textures", [])),
            "animations": len(doc.get("animations", [])),
            "nodes": len(doc.get("nodes", [])),
            "quality_warning": "Metadata validation only; not a render/performance/rigging certification"}


def inspect_asset(filename: str, displayed_css_width: int = 0, dpr: float = 2) -> dict:
    """Inspect one approved original file; files never leave the local asset directory."""
    if not isinstance(filename, str) or not NAME.fullmatch(filename):
        raise ValueError("Use a simple allowed filename")
    if not isinstance(displayed_css_width, int) or not 0 <= displayed_css_width <= 7680:
        raise ValueError("CSS width out of approved range")
    if not isinstance(dpr, (int, float)) or not 1 <= dpr <= 4:
        raise ValueError("DPR out of approved range")

    ext = Path(filename).suffix.lower()
    if ext == ".glb":
        root = asset_root()
        path = (root / filename).resolve(strict=True)
        if path.parent != root or not path.is_file():
            raise ValueError("GLB outside approved directory")
        return {"filename": filename, **_glb(path)}
    if ext not in {".png", ".jpg", ".jpeg", ".webp", ".svg"}:
        raise ValueError("Unsupported format")
    path = _allowed_asset(filename)
    if ext == ".svg":
        return {"filename": filename, **_read_svg(path)}
    size = _size(path)
    dims = {".png": _png_dimensions, ".jpg": _jpeg_dimensions,
            ".jpeg": _jpeg_dimensions, ".webp": _webp_dimensions}
    w, h = dims[ext](path)
    if w <= 0 or h <= 0 or w * h > 500_000_000:
        raise ValueError("Implausible raster dimensions")
    min_width = int(displayed_css_width * float(dpr))
    return {"filename": filename, "type": ext[1:], "bytes": size,
            "intrinsic_width": w, "intrinsic_height": h,
            "displayed_css_width": displayed_css_width, "target_dpr": float(dpr),
            "min_intrinsic_width_for_density": min_width,
            "density_pass": bool(w >= min_width) if displayed_css_width else None,
            "does_not_claim_8k": True}
