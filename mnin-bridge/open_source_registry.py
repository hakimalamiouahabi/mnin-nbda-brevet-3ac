"""Verified public GitHub toolchain registry for MNIN Bridge.

A GitHub repository is a SOURCE, not an installed ChatGPT plugin.
The catalogue never clones, downloads or executes third-party code.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

REGISTRY = Path(__file__).parent / "integrations" / "open_source_registry.json"
SAFE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
LICENSES = {"MIT", "Apache-2.0", "ISC", "MPL-2.0"}
STATUS = {"already_integrated_code", "proposed_runtime_dependency",
          "catalogued", "catalogued_read_only", "existing_python_dependency"}


def _load_and_validate() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0.0":
        raise ValueError("Unsupported open source registry schema")
    projects = data.get("projects")
    if not isinstance(projects, list) or len(projects) != 11:
        raise ValueError("Expected exactly eleven vetted projects")
    seen = set()
    for item in projects:
        id = item.get("id", "")
        uri = urlsplit(item.get("url", ""))
        if not SAFE.fullmatch(id) or id in seen:
            raise ValueError("Invalid or duplicate repository ID")
        if (uri.scheme, uri.netloc, uri.path) != ("https", "github.com", "/" + id):
            raise ValueError("A registered source must be a literal GitHub HTTPS repository")
        if uri.username or uri.password or uri.query or uri.fragment:
            raise ValueError("Credentials, query and fragments are prohibited")
        if item.get("license") not in LICENSES:
            raise ValueError("License type not in reviewed allowlist")
        if item.get("connection_status") not in STATUS:
            raise ValueError("Unknown connection state")
        if item.get("visibility_verified") != "public" or item.get("archived") is not False:
            raise ValueError("Repository verification flags missing")
        seen.add(id)
    return data


def list_upstreams(domain: str = "") -> dict:
    data = _load_and_validate()
    projects = data["projects"]
    if domain:
        if not isinstance(domain, str) or len(domain) > 100 or not re.fullmatch(r"[A-Za-z0-9_ -]+", domain):
            raise ValueError("Invalid domain filter")
        projects = [p for p in projects if p["domain"].lower() == domain.lower()]
    result = [
        {k: p[k] for k in ("id", "url", "license", "domain",
                            "purpose", "connection_status", "package", "pinned_version")}
        for p in projects
    ]
    return {"count": len(result), "projects": result,
            "actually_linked_to_chatgpt_pro": False,
            "note": "Code repository linked in project registry, not yet an authenticated MCP connection or a running tool"}


def readiness() -> dict:
    data = _load_and_validate()
    status = {}
    for p in data["projects"]:
        state = p["connection_status"]
        status[state] = status.get(state, 0) + 1
    return {
        "registered_projects": len(data["projects"]),
        "statuses": status,
        "runner_npm_dependency_manifest_present":
            (Path(__file__).parent / "runner" / "package.json").is_file(),
        "github_repos_are_plugins": False,
        "remote_mcp_endpoint_active": False,
        "oauth_identity_verified": False,
    }
