"""MNIN Bridge Pro v0.6: bounded static QA of *local* HTML copies.

Read-only, offline, standard-library only. No browser, WordPress access, network
requests, JavaScript execution or claims of WCAG/Core Web Vitals certification.
Only home/, site/ or preview/ below an explicitly mounted private root.
"""
from __future__ import annotations

import hashlib
import os
import re
import struct
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ALLOWED_TOP = frozenset({"home", "site", "preview"})
MAX_HTML_BYTES = 2 * 1024 * 1024
MAX_IMAGES = 80
MAX_IMAGE_BYTES = 40 * 1024 * 1024
ASSET_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".webp", ".svg"})
LANG_RE = re.compile(r"^(fr|ar)(-[A-Za-z0-9]+)*$", re.I)


class _PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.direction = ""
        self.h1 = 0
        self.title_seen = False
        self.has_title_text = False
        self.in_title = False
        self.meta_description = False
        self.viewport = False
        self.images = []
        self.ids = set()
        self.duplicate_ids = []
        self.fragment_links = []
        self.labels = 0
        self.buttons = 0
        self.forms = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang") or ""
            self.direction = attrs.get("dir") or ""
        if tag == "title":
            self.title_seen = True
            self.in_title = True
        if tag == "h1":
            self.h1 += 1
        if tag == "meta":
            if (attrs.get("name") or "").lower() == "description" and (attrs.get("content") or "").strip():
                self.meta_description = True
            if attrs.get("name", "").lower() == "viewport":
                self.viewport = True
        if tag == "img":
            self.images.append(attrs)
        if tag == "a" and (attrs.get("href") or "").startswith("#") and len(attrs["href"]) > 1:
            self.fragment_links.append(unquote(attrs["href"][1:]))
        if "id" in attrs and attrs["id"]:
            if attrs["id"] in self.ids:
                self.duplicate_ids.append(attrs["id"])
            self.ids.add(attrs["id"])
        if tag == "label":
            self.labels += 1
        if tag == "button":
            self.buttons += 1
        if tag == "form":
            self.forms += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and data.strip():
            self.has_title_text = True


def _root() -> Path:
    raw = os.environ.get("MNIN_SITE_ROOT", "")
    if not raw:
        raise RuntimeError("BLOQUE: MNIN_SITE_ROOT (a private, mounted copy) is not configured")
    root = Path(raw).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("MNIN_SITE_ROOT must be a directory")
    return root


def _within(root: Path, path: Path) -> bool:
    return path == root or root in path.parents


def _page(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or len(relative) > 240 or "\\" in relative:
        raise ValueError("Invalid relative HTML path")
    parts = Path(relative).parts
    if len(parts) < 2 or parts[0] not in ALLOWED_TOP or any(p in (".", "..") for p in parts):
        raise ValueError("Expected home/, site/ or preview/ local path")
    if not relative.lower().endswith(".html") or Path(relative).is_absolute():
        raise ValueError("Expected local .html file")
    path = root.joinpath(*parts)
    if not _within(root, path.resolve(strict=True)) or path.is_symlink() or not path.is_file():
        raise ValueError("HTML must be a regular, confined file")
    if path.stat().st_size > MAX_HTML_BYTES:
        raise ValueError("HTML file exceeds size limit")
    return path


def _local_image(root: Path, html_path: Path, src: str):
    if not src or len(src) > 1024 or "\\" in src:
        return "INVALID", None
    parts = urlsplit(src)
    if parts.scheme or parts.netloc or src.startswith("//"):
        return "EXTERNAL_UNVERIFIED", None
    name = unquote(parts.path)
    if not name or "\x00" in name:
        return "INVALID", None
    if name.startswith("/"):
        candidate = root / name.lstrip("/")
    else:
        candidate = html_path.parent / name
    try:
        path = candidate.resolve(strict=False)
    except (OSError, RuntimeError):
        return "INVALID", None
    if not _within(root, path) or candidate.is_symlink():
        return "REJECTED_OUT_OF_SCOPE", None
    if path.suffix.lower() not in ASSET_SUFFIXES:
        return "UNSUPPORTED", None
    if not path.exists():
        return "MISSING_LOCAL", None
    if not path.is_file() or path.stat().st_size > MAX_IMAGE_BYTES:
        return "REJECTED_OUT_OF_SCOPE", None
    return "LOCAL", path


def _dimensions(path: Path) -> tuple[int, int] | None:
    """Parse dimensions from bounded headers; no image decoder or SVG XML parsing."""
    with path.open("rb") as handle:
        b = handle.read(262144)
    suffix = path.suffix.lower()
    if suffix == ".png" and len(b) >= 24 and b[:8] == b"\x89PNG\r\n\x1a\n" and b[12:16] == b"IHDR":
        return struct.unpack(">II", b[16:24])
    if suffix == ".webp" and len(b) >= 30 and b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        if b[12:16] == b"VP8X":
            return 1 + int.from_bytes(b[24:27], "little"), 1 + int.from_bytes(b[27:30], "little")
        if b[12:16] == b"VP8 " and b[23:26] == b"\x9d\x01\x2a":
            return int.from_bytes(b[26:28], "little") & 0x3fff, int.from_bytes(b[28:30], "little") & 0x3fff
        if b[12:16] == b"VP8L" and b[20] == 0x2f:
            v = int.from_bytes(b[21:25], "little")
            return (v & 0x3fff) + 1, ((v >> 14) & 0x3fff) + 1
    if suffix in (".jpg", ".jpeg") and len(b) > 4 and b[:2] == b"\xff\xd8":
        i = 2
        while i + 4 < len(b):
            if b[i] != 0xff:
                i += 1
                continue
            while i < len(b) and b[i] == 0xff:
                i += 1
            if i >= len(b):
                break
            marker = b[i]
            i += 1
            if marker in (0xd8, 0xd9, 0x01) or 0xd0 <= marker <= 0xd7:
                continue
            if marker == 0xda or i + 2 > len(b):
                break
            length = int.from_bytes(b[i:i + 2], "big")
            if length < 2 or i + length > len(b):
                break
            if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf) and length >= 7:
                return int.from_bytes(b[i+5:i+7], "big"), int.from_bytes(b[i+3:i+5], "big")
            i += length
    return None


def _hash(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


REMEDIATIONS = {
    "BROKEN_LOCAL_IMAGE": ("P0", "FRONTEND_UI", "Restore or correct a missing local image"),
    "IMAGE_OUT_OF_SCOPE": ("P0", "SECURITY_PRIVACY", "Inspect image path confinement and source provenance"),
    "RTL_NOT_DECLARED": ("P1", "LOCALIZATION_FR_AR", "Align document direction with Arabic language"),
    "IMG_ALT_MISSING": ("P1", "UX_ACCESSIBILITY", "Write functional or informative alt text; decorative images need alt empty"),
    "RASTER_DPR_WARNING": ("P1", "ILLUSTRATION_MOTION", "Supply a verifiable high-density original or appropriate vector"),
    "H1_COUNT": ("P1", "FRONTEND_UI", "Correct the single-main-heading hierarchy"),
    "DUPLICATE_ID": ("P1", "FRONTEND_UI", "Ensure unique HTML identifiers"),
    "BROKEN_FRAGMENT": ("P1", "FRONTEND_UI", "Repair local in-page anchor references"),
    "VIEWPORT_MISSING": ("P1", "RESPONSIVE_MOBILE", "Add a valid responsive viewport meta tag"),
    "LANG_MISSING_OR_UNSUPPORTED": ("P1", "LOCALIZATION_FR_AR", "Declare the correct HTML document language"),
    "TITLE_MISSING": ("P1", "SEO_GROWTH", "Provide an accurate document title"),
    "IMAGE_SCAN_TRUNCATED": ("P1", "QA_AUTOMATION", "Split audit into bounded page sections and inspect remaining images"),
    "IMG_DIMENSIONS_NOT_DECLARED": ("P2", "PERFORMANCE_WP", "Define image dimensions or aspect-ratio for layout stability"),
    "META_DESCRIPTION_MISSING": ("P2", "SEO_GROWTH", "Provide a verified human-friendly page description"),
}

def _triage(issues: list[dict]) -> list[dict]:
    counts = {}
    for issue in issues:
        code = issue["code"]
        counts[code] = counts.get(code, 0) + 1
    steps = []
    for code, count in counts.items():
        priority, specialist, recommendation = REMEDIATIONS.get(
            code, ("P2", "QA_AUTOMATION", "Review the warning with actual evidence")
        )
        steps.append({"priority": priority, "issue_code": code, "occurrences": count,
                      "specialist": specialist, "recommendation": recommendation,
                      "evidence_status": "NON TESTÉ", "changed_files": 0})
    return sorted(steps, key=lambda item: (item["priority"], item["issue_code"]))


def audit_local_home(relative_html: str, target_dpr: int = 2) -> dict:
    if type(target_dpr) is not int or target_dpr not in (1, 2, 3):
        raise ValueError("Target DPR must be 1, 2 or 3")
    root = _root()
    page = _page(root, relative_html)
    html = page.read_text(encoding="utf-8", errors="replace")
    parser = _PageParser()
    parser.feed(html)
    issues = []
    def issue(code, severity, detail):
        issues.append({"code": code, "severity": severity, "detail": detail})
    if not parser.lang or not LANG_RE.match(parser.lang):
        issue("LANG_MISSING_OR_UNSUPPORTED", "warning", "Declare fr or ar language in html lang")
    if parser.lang.lower().startswith("ar") and parser.direction.lower() != "rtl":
        issue("RTL_NOT_DECLARED", "warning", "Arabic HTML should declare dir=rtl")
    if parser.h1 != 1:
        issue("H1_COUNT", "warning", f"Exactly one H1 expected, found {parser.h1}")
    if not parser.has_title_text:
        issue("TITLE_MISSING", "warning", "Add a nonempty HTML title")
    if not parser.viewport:
        issue("VIEWPORT_MISSING", "warning", "Missing viewport meta for responsive behavior")
    if not parser.meta_description:
        issue("META_DESCRIPTION_MISSING", "notice", "No nonempty meta description found")
    for ident in sorted(set(parser.duplicate_ids))[:30]:
        issue("DUPLICATE_ID", "warning", "Duplicated HTML id: " + ident[:80])
    for ident in sorted(set(parser.fragment_links) - parser.ids)[:30]:
        issue("BROKEN_FRAGMENT", "warning", "Link references absent fragment: " + ident[:80])

    records = []
    for number, attrs in enumerate(parser.images[:MAX_IMAGES], start=1):
        source = attrs.get("src") or ""
        record = {"index": number, "source": source[:200], "alt_attribute_present": "alt" in attrs}
        if "alt" not in attrs:
            issue("IMG_ALT_MISSING", "warning", "Image " + str(number) + " lacks alt attribute")
        if "width" not in attrs or "height" not in attrs:
            issue("IMG_DIMENSIONS_NOT_DECLARED", "notice", "Image " + str(number) + " lacks width/height attributes (layout-shift risk heuristic)")
        if not source and attrs.get("srcset"):
            record["asset_status"] = "SRCSET_NOT_INSPECTED"
            records.append(record)
            continue
        status, path = _local_image(root, page, source)
        record["asset_status"] = status
        if status == "MISSING_LOCAL":
            issue("BROKEN_LOCAL_IMAGE", "error", "Local image " + str(number) + " not found")
        elif status == "REJECTED_OUT_OF_SCOPE":
            issue("IMAGE_OUT_OF_SCOPE", "warning", "Image " + str(number) + " is outside approved assets")
        if path:
            record["bytes"] = path.stat().st_size
            record["sha256"] = _hash(path)
            record["type"] = path.suffix.lower()
            dims = _dimensions(path)
            if dims:
                record["native_pixels"] = {"width": dims[0], "height": dims[1]}
                try:
                    declared = int(attrs.get("width", ""))
                except (ValueError, TypeError):
                    declared = 0
                if declared > 0 and dims[0] < declared * target_dpr:
                    issue("RASTER_DPR_WARNING", "warning",
                          f"Image {number}: native width {dims[0]} less than HTML width {declared} x DPR {target_dpr} (CSS may override)")
            elif path.suffix.lower() == ".svg":
                record["vector"] = True
                record["note"] = "SVG resolution-independent in principle; content and rendering not inspected"
            else:
                record["dimensions"] = "UNVERIFIED"
        records.append(record)
    if len(parser.images) > MAX_IMAGES:
        issue("IMAGE_SCAN_TRUNCATED", "warning", f"Only first {MAX_IMAGES} images inspected")
    return {
        "version": "0.6.0",
        "type": "READ_ONLY_STATIC_LOCAL_HTML",
        "source": relative_html,
        "target_dpr": target_dpr,
        "page_sha256": _hash(page),
        "summary": {"total_images": len(parser.images), "inspected_images": len(records),
                    "h1_count": parser.h1, "html_lang": parser.lang, "html_dir": parser.direction,
                    "errors": sum(i["severity"] == "error" for i in issues),
                    "warnings": sum(i["severity"] == "warning" for i in issues),
                    "notices": sum(i["severity"] == "notice" for i in issues)},
        "images": records,
        "issues": issues[:200],
        "remediation_plan": _triage(issues),
        "evidence_quality": "Static heuristic only. No runtime browser, WCAG certification, Core Web Vitals or pixel-perfect comparison.",
        "execution": "NO_NETWORK_NO_WORDPRESS_WRITES",
    }
