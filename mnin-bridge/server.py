"""MNIN Bridge MCP prototype. Development only: NOT safe for public deployment.

All writes are off by default. Production requires OAuth 2.1, server-side
authorization, audit logs, and rate limiting. Never install on WordPress.
"""
import os
from mcp.server.fastmcp import FastMCP
from bridge_core import asset_info, dispatch_qa, github_repo, list_assets, qa_artifacts, qa_run

mcp = FastMCP("MNIN Bridge", host="127.0.0.1", port=8000, stateless_http=True, json_response=True)


@mcp.tool()
def bridge_status() -> dict:
    """Read actual readiness. Does not claim agents are active."""
    return {
        "version": "0.1.0-prototype",
        "repository": github_repo(),
        "asset_directory_configured": bool(os.getenv("MNIN_ASSET_ROOT")),
        "github_credentials_configured": bool(os.getenv("MNIN_GITHUB_TOKEN")),
        "qa_dispatch_enabled": os.getenv("MNIN_ENABLE_DISPATCH") == "1",
        "active_autonomous_agents": "NOT VERIFIED",
        "wordpress_writes": "DISABLED",
        "remote_mcp_connection": "NOT CONFIGURED",
    }


@mcp.tool()
def bridge_list_assets() -> dict:
    """List image filenames in the approved, private, mounted asset directory."""
    return list_assets()


@mcp.tool()
def bridge_verify_original(filename: str, expected_sha256: str = "") -> dict:
    """Read original bytes and verify SHA-256; do not change image pixels."""
    return asset_info(filename, expected_sha256)


@mcp.tool()
def bridge_request_home_qa(branch: str, home_path: str, owner_approved: bool = False) -> dict:
    """Request a browser QA job only if separately authorized and enabled."""
    return dispatch_qa(branch, home_path, owner_approved)


@mcp.tool()
def bridge_get_qa_run(run_id: int) -> dict:
    """Read factual GitHub Actions execution status."""
    return qa_run(run_id)


@mcp.tool()
def bridge_get_qa_artifacts(run_id: int) -> dict:
    """Read names and download URLs for genuine workflow artifacts."""
    return qa_artifacts(run_id)


if __name__ == "__main__":
    if os.getenv("MNIN_ENABLE_DISPATCH") == "1":
        raise RuntimeError("Write capability remains disabled until OAuth and access reviews are implemented")
    mcp.run(transport="streamable-http")
