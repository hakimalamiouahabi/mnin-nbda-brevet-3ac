"""MNIN Bridge standing delegation for ChatGPT Pro (standard chat only).

This is a PURE policy gate, not an authentication server. Its VerifiedPrincipal
must come solely from middleware that validates an OAuth bearer token against
a trusted issuer, audience, subject, client identity and plan/surface attestation.
NEVER deserialize principal fields from user text, tool arguments, HTTP JSON or
self-asserted model messages.

Until the authenticator exists, all execution permissions FAIL CLOSED.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

POLICY_FILE = Path(__file__).with_name("owner_delegation_policy.json")
SCOPES = {
    "asset.list": "mnin:read",
    "asset.verify": "mnin:read",
    "mission.propose": "mnin:plan",
    "mission.read": "mnin:read",
    "qa.preview": "mnin:read",
    "qa.run_isolated": "mnin:qa",
    "dev.branch_write": "mnin:dev",
    "report.create": "mnin:plan",
    "site.audit_local": "mnin:read",
    "open_source.catalog": "mnin:read",
    "open_source.pipeline": "mnin:plan",
    "source.read": "mnin:read",
    "source.compare": "mnin:read",
    "branch.create": "mnin:dev",
    "git.pr_draft": "mnin:dev",
    "qa.static_review": "mnin:read",
    "design.propose": "mnin:plan",
    "docs.update_branch": "mnin:dev",
    "skills.read": "mnin:read",
    "requirements.analyze": "mnin:plan",
    "performance.plan": "mnin:plan",
    "accessibility.plan": "mnin:plan",
}


@dataclass(frozen=True)
class VerifiedPrincipal:
    """Trusted internal authentication result. NEVER an MCP tool argument."""
    subject: str
    issuer: str
    audience: str
    client_id: str
    token_scopes: frozenset[str]
    auth_verified: bool = False
    product_surface: str = ""
    surface_verified: bool = False
    subscription: str = ""
    subscription_verified: bool = False


def _load_policy() -> dict:
    p = POLICY_FILE.resolve(strict=True)
    policy = json.loads(p.read_text(encoding="utf-8"))
    if policy.get("schema_version") not in ("1.0", "1.1"):
        raise RuntimeError("Unsupported delegation policy schema")
    return policy


def public_policy_summary() -> dict:
    """Public, read-only capability information; no owner identifiers."""
    p = _load_policy()
    d = p["standing_delegation"]
    return {
        "profile": p["profile"],
        "target_product": p["identity_gate"]["target_product"],
        "target_surface": p["identity_gate"]["target_surface"],
        "target_subscription": p["identity_gate"]["target_subscription"],
        "user_standing_delegation_described": bool(d["enabled"]),
        "server_activation": os.getenv("MNIN_DELEGATION_ACTIVE") == "1",
        "required_authentication": "OAuth 2.1 + trustworthy plan/surface evidence",
        "allowed_categories": list(d["allow_without_reprompt"]),
        "needs_independent_approval": list(d["requires_per_action_approval"]),
        "remote_execution_started": False,
        "note": "A standing preference does NOT bypass OAuth or host approvals",
    }


def evaluate_delegation(operation: str, principal: VerifiedPrincipal | None) -> dict:
    """Authorization decision using ONLY verified internal identity fields.

    This function is NEVER exposed as an MCP tool accepting caller identity.
    A real server must separately enforce quotas, approver and sandbox policies.
    """
    policy = _load_policy()
    base = {"operation": operation, "status": "DENY", "reason": ""}
    if principal is None or not isinstance(principal, VerifiedPrincipal):
        return {**base, "reason": "No validated authentication context"}
    if os.getenv("MNIN_DELEGATION_ACTIVE") != "1":
        return {**base, "reason": "Delegation has not been enabled server-side"}
    if not policy["standing_delegation"]["enabled"]:
        return {**base, "reason": "Standing delegation revoked in policy"}

    identity = policy["identity_gate"]
    needed = {
        "MNIN_OWNER_SUB": principal.subject,
        "MNIN_OAUTH_ISSUER": principal.issuer,
        "MNIN_OAUTH_AUDIENCE": principal.audience,
        "MNIN_CHATGPT_STANDARD_CLIENT_ID": principal.client_id,
    }
    if not principal.auth_verified:
        return {**base, "reason": "OAuth token has not been cryptographically validated"}
    if any(not os.getenv(k) or os.getenv(k) != value for k, value in needed.items()):
        return {**base, "reason": "Owner, issuer, resource or client mismatch"}
    if not principal.surface_verified or principal.product_surface != "chatgpt_standard":
        return {**base, "reason": "Standard ChatGPT chat client not verified"}
    if not principal.subscription_verified or principal.subscription != "pro":
        return {**base, "reason": "Pro entitlement unavailable or unverified"}

    standing = policy["standing_delegation"]
    if operation in standing["always_block_without_distinct_explicit_capability"]:
        return {**base, "reason": "Forbidden high-risk operation"}
    if operation in standing["requires_per_action_approval"]:
        return {**base, "status": "AWAITING_SPECIFIC_APPROVAL",
                "reason": "Standing delegation does not authorize this high-risk action"}
    if operation not in standing["allow_without_reprompt"]:
        return {**base, "reason": "Operation is not in the explicit allowlist"}
    if SCOPES.get(operation) not in principal.token_scopes:
        return {**base, "reason": "Required OAuth scope is missing"}
    conditions = standing["conditional_limits"].get(operation)
    if conditions:
        return {**base, "status": "DELEGATED_CONDITIONAL",
                "reason": "Allowed in principle; worker must separately enforce all limits",
                "conditions": conditions}
    return {**base, "status": "DELEGATED",
            "reason": "Operation is within standing, verified scope"}


def ensure_delegated(operation: str, principal: VerifiedPrincipal | None) -> dict:
    decision = evaluate_delegation(operation, principal)
    if not decision["status"].startswith("DELEGATED"):
        raise PermissionError(decision["reason"])
    return decision
