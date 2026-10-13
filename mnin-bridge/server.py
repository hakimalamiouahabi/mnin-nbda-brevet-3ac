"""MNIN Bridge MCP prototype. Development only: NOT safe for public deployment.

All writes are off by default. Production requires OAuth 2.1, server-side
authorization, audit logs, and rate limiting. Never install on WordPress.
"""
import os
from mcp.server.fastmcp import FastMCP
from bridge_core import asset_info, dispatch_qa, github_repo, list_assets, qa_artifacts, qa_run
from mission_control import MissionStore, capability_catalog, validate_request
from access_policy import public_policy_summary
from quality_lab import inspect_asset
from open_source_registry import list_upstreams, readiness
from db_guardian import (audit_sqlite_snapshot, preview_cleanup, wordpress_readonly_plan, github_readonly_plan, cloudflare_readonly_plan, maintenance_guardrails)
from agentgrid import AgentGrid, roster_status
from role_briefs import role_brief

mcp = FastMCP("MNIN Bridge", host="127.0.0.1", port=8000, stateless_http=True, json_response=True)


def _require_verified_pro_standard_chat() -> None:
    """OAuth integration is not implemented. NEVER trust user/model-supplied claims."""
    raise PermissionError("Protected tools disabled: OAuth, Pro entitlement and standard chat client attestation are not verified")


@mcp.tool()
def bridge_status() -> dict:
    """Read actual readiness. Does not claim agents are active."""
    return {
        "version": "0.8.0-prototype",
        "repository": github_repo(),
        "asset_directory_configured": bool(os.getenv("MNIN_ASSET_ROOT")),
        "github_credentials_configured": bool(os.getenv("MNIN_GITHUB_TOKEN")),
        "qa_dispatch_enabled": False,  # No independent OAuth approval system yet
        "active_autonomous_agents": "NOT VERIFIED",
        "wordpress_writes": "DISABLED",
        "remote_mcp_connection": "NOT CONFIGURED",
    }


@mcp.tool()
def bridge_list_assets() -> dict:
    """List image filenames in the approved, private, mounted asset directory."""
    _require_verified_pro_standard_chat()
    return list_assets()


@mcp.tool()
def bridge_verify_original(filename: str, expected_sha256: str = "") -> dict:
    """Read original bytes and verify SHA-256; do not change image pixels."""
    _require_verified_pro_standard_chat()
    return asset_info(filename, expected_sha256)


@mcp.tool()
def bridge_request_home_qa(branch: str, home_path: str, owner_approved: bool = False) -> dict:
    """Request a browser QA job only if separately authorized and enabled."""
    raise RuntimeError("QA execution disabled in v0.2 until independent authenticated approval is implemented")


@mcp.tool()
def bridge_get_qa_run(run_id: int) -> dict:
    """Read factual GitHub Actions execution status."""
    _require_verified_pro_standard_chat()
    return qa_run(run_id)


@mcp.tool()
def bridge_get_qa_artifacts(run_id: int) -> dict:
    """Read names and download URLs for genuine workflow artifacts."""
    _require_verified_pro_standard_chat()
    return qa_artifacts(run_id)


def _local_store() -> MissionStore:
    # Local-only prototype. No public internet deployment before OAuth review.
    if os.getenv("MNIN_ENABLE_LOCAL_MISSIONS") != "1":
        raise RuntimeError("Mission store disabled pending authenticated deployment")
    return MissionStore()


@mcp.tool()
def bridge_capability_catalog() -> dict:
    """List supported MNIN missions and their REAL execution readiness."""
    return capability_catalog()


@mcp.tool()
def bridge_validate_mission(kind: str, inputs: dict) -> dict:
    """Validate a proposed mission without making any changes."""
    return {"kind": kind, "validated_inputs": validate_request(kind, inputs),
            "execution": "NOT STARTED"}


@mcp.tool()
def bridge_propose_mission(kind: str, inputs: dict, idempotency_key: str = "") -> dict:
    """Store a planned mission locally. DOES NOT execute code, deploy or spawn agents."""
    _require_verified_pro_standard_chat()
    return _local_store().propose(kind, inputs, idempotency_key)


@mcp.tool()
def bridge_list_missions(limit: int = 20) -> list[dict]:
    """Read recorded mission proposals. Local authorization still required."""
    _require_verified_pro_standard_chat()
    return _local_store().list(limit)


@mcp.tool()
def bridge_get_mission(mission_id: str) -> dict:
    """Read one mission, without execution."""
    _require_verified_pro_standard_chat()
    return _local_store().read(mission_id)


@mcp.tool()
def bridge_preview_mission(mission_id: str) -> dict:
    """Show planned roles, blockers, evidence requirements and scope."""
    _require_verified_pro_standard_chat()
    return _local_store().preview(mission_id)


@mcp.tool()
def bridge_mission_audit(mission_id: str) -> list[dict]:
    """Read recorded audit events from the local mission store."""
    _require_verified_pro_standard_chat()
    return _local_store().audit(mission_id)


@mcp.tool()
def bridge_delegation_policy() -> dict:
    """Read non-sensitive scope of durable user delegation (never changes permissions)."""
    return public_policy_summary()


@mcp.tool()
def bridge_inspect_production_asset(filename: str, displayed_css_width: int = 0, dpr: float = 2) -> dict:
    """Inspect a private PNG/JPEG/WebP/SVG/GLB original without editing or uploading it."""
    _require_verified_pro_standard_chat()
    return inspect_asset(filename, displayed_css_width, dpr)


@mcp.tool()
def bridge_open_source_catalog(domain: str = "") -> dict:
    """List 11 verified public free/open-source GitHub integrations; no cloning or execution."""
    return list_upstreams(domain)


@mcp.tool()
def bridge_open_source_readiness() -> dict:
    """Report registered vs actually connected OSS components without fabricating readiness."""
    return readiness()


@mcp.tool()
def bridge_sqlite_snapshot_audit(filename: str) -> dict:
    """Audit an authorized offline SQLite snapshot; never inspect or change row-level data."""
    _require_verified_pro_standard_chat()
    return audit_sqlite_snapshot(filename)


@mcp.tool()
def bridge_cleanup_dry_run(context: str, candidates: list[dict]) -> dict:
    """Prepare a NON-EXECUTING cleanup plan for D1, WordPress or GitHub."""
    return preview_cleanup(context, candidates)


@mcp.tool()
def bridge_wordpress_cleanup_plan() -> dict:
    """Show allowed read-only WP-CLI checks and blocked cleanup commands."""
    return wordpress_readonly_plan()


@mcp.tool()
def bridge_github_cleanup_plan(repository: str) -> dict:
    """Show GitHub cleanup audit steps without rewriting history or deleting branches."""
    return github_readonly_plan(repository)


@mcp.tool()
def bridge_cloudflare_cleanup_plan(database: str) -> dict:
    """Show Cloudflare D1 cleanup audit steps; no live SQL is executed by this tool."""
    return cloudflare_readonly_plan(database)


@mcp.tool()
def bridge_maintenance_safety_limits() -> dict:
    """Read fail-closed D1, GitHub and WordPress cleanup safety ceilings."""
    return maintenance_guardrails()


@mcp.tool()
def bridge_agentgrid_700_status() -> dict:
    """Verified distribution of the original 700 MNIN roles; no agents are running."""
    return roster_status()


@mcp.tool()
def bridge_agentgrid_search_roles(term: str, limit: int = 12) -> list[dict]:
    """Search the original 700 role titles and competency groups (read only)."""
    return AgentGrid().search(term, limit)


@mcp.tool()
def bridge_agentgrid_plan_mission(mission_kind: str, expert_limit: int = 9) -> dict:
    """Select existing DSI/managers/team leaders/experts; planning, NOT AI execution."""
    return AgentGrid().route(mission_kind, expert_limit)


@mcp.tool()
def bridge_agentgrid_plan_portfolio(mission_kinds: list[str], expert_limit: int = 6, max_concurrent_jobs: int = 2) -> dict:
    """Plan up to five controlled jobs with existing roles; never spawn 700 LLMs."""
    return AgentGrid().portfolio(mission_kinds, expert_limit, max_concurrent_jobs)


@mcp.tool()
def bridge_agentgrid_role_brief(profile_id: str, mission_kind: str = "") -> dict:
    """Retrieve an approved existing professional role contract. Not a new AI session."""
    return role_brief(profile_id, mission_kind)


if __name__ == "__main__":
    if os.getenv("MNIN_ENABLE_DISPATCH") == "1":
        raise RuntimeError("Write capability remains disabled until OAuth and access reviews are implemented")
    mcp.run(transport="streamable-http")
