"""MNIN Bridge: guarded access to originals and GitHub Actions."""
import hashlib, json, os, re, struct
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_DEFAULT = "hakimalamiouahabi/mnin-nbda-brevet-3ac"
WORKFLOW = "mnin-bridge-home-qa.yml"
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,159}$")
BRANCH = re.compile(r"^(feature|proposal)/[A-Za-z0-9][A-Za-z0-9._/-]{0,110}$")
HOME = re.compile(r"^(site|home|preview)/[A-Za-z0-9_.\-/]+\.html$")
HASH = re.compile(r"^[a-fA-F0-9]{64}$")
EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".svg"}


def asset_root():
    raw = os.getenv("MNIN_ASSET_ROOT")
    if not raw:
        raise RuntimeError("MNIN_ASSET_ROOT is not configured")
    path = Path(raw).expanduser().resolve(strict=True)
    if not path.is_dir():
        raise ValueError("Asset root must be a directory")
    return path


def _allowed_asset(filename):
    if not NAME.fullmatch(filename) or Path(filename).suffix.lower() not in EXTENSIONS:
        raise ValueError("Expected a simple image filename (no directory)")
    root = asset_root()
    path = (root / filename).resolve(strict=True)
    if path.parent != root or not path.is_file():
        raise ValueError("Asset must be in the approved private directory")
    if path.stat().st_size > 100 * 1024 * 1024:
        raise ValueError("File exceeds 100 MB limit")
    return path


def asset_info(filename, expected_sha256=""):
    """Compute digest without rewriting, regenerating or resizing an original."""
    if expected_sha256 and not HASH.fullmatch(expected_sha256):
        raise ValueError("Expected SHA-256 must be 64 hex chars")
    path = _allowed_asset(filename)
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(part)
    digest = hasher.hexdigest()
    result = {"filename": path.name, "bytes": path.stat().st_size, "sha256": digest}
    if path.suffix.lower() == ".png":
        with path.open("rb") as f:
            header = f.read(24)
        if header[:8] == b"\x89PNG\r\n\x1a\n" and header[12:16] == b"IHDR":
            w, h = struct.unpack(">II", header[16:24])
            result["dimensions"] = {"width": w, "height": h}
    if expected_sha256:
        result["matches_expected"] = digest.lower() == expected_sha256.lower()
    return result


def list_assets():
    root = asset_root()
    names = sorted(p.name for p in root.iterdir()
                   if p.is_file() and not p.is_symlink()
                   and NAME.fullmatch(p.name) and p.suffix.lower() in EXTENSIONS)
    return {"total": len(names), "files": names[:100],
            "note": "No originals are uploaded to GitHub"}


def validate_dispatch(branch, home_path):
    if not BRANCH.fullmatch(branch) or ".." in branch:
        raise ValueError("Only feature/ or proposal/ branches are allowed")
    if not HOME.fullmatch(home_path) or ".." in home_path:
        raise ValueError("HTML must be within site/, home/ or preview/")


def github_repo():
    repo = os.getenv("MNIN_GITHUB_REPOSITORY", REPO_DEFAULT)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise ValueError("Invalid GitHub repository")
    return repo


def github_api(method, path, payload=None):
    token = os.getenv("MNIN_GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GitHub token not configured")
    if not path.startswith("/") or ".." in path or "://" in path:
        raise ValueError("Invalid API path")
    body = json.dumps(payload).encode() if payload is not None else None
    req = Request(
        "https://api.github.com/repos/" + github_repo() + path,
        data=body, method=method,
        headers={"Authorization": "Bearer " + token,
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "User-Agent": "MNIN-Bridge/0.1",
                 **({"Content-Type": "application/json"} if body else {})})
    try:
        with urlopen(req, timeout=20) as res:
            data = res.read(1024 * 1024)
            return {"status": res.status, "data": json.loads(data) if data else {}}
    except HTTPError as e:
        raise RuntimeError("GitHub API HTTP " + str(e.code)) from None
    except URLError:
        raise RuntimeError("GitHub API unreachable") from None


def dispatch_qa(branch, home_path, owner_approved=False):
    validate_dispatch(branch, home_path)
    # Model-provided owner_approved is never accepted as authorization.
    # No public MCP write tool is exposed until real OAuth user approval exists.
    raise RuntimeError("QA dispatch is hard-disabled pending out-of-band authorization")


def qa_run(run_id):
    if not isinstance(run_id, int) or run_id <= 0:
        raise ValueError("run_id must be a positive integer")
    d = github_api("GET", "/actions/runs/" + str(run_id))["data"]
    return {k: d.get(k) for k in
            ("id", "name", "status", "conclusion", "html_url", "run_started_at", "updated_at")}


def qa_artifacts(run_id):
    if not isinstance(run_id, int) or run_id <= 0:
        raise ValueError("run_id must be a positive integer")
    d = github_api("GET", "/actions/runs/" + str(run_id) + "/artifacts")["data"]
    return {"artifacts": [{k: a.get(k) for k in
            ("id", "name", "size_in_bytes", "expired", "archive_download_url")}
            for a in d.get("artifacts", [])]}
