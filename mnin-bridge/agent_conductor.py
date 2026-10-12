"""MNIN Bridge Pro: evidence-first DSI mission conductor (v0.5).

Read-only deterministic mission blueprint. ChatGPT Pro is the reasoning engine:
this file DOES NOT spawn agents, obtain privileges, or execute external changes.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from premium_suite import MODULES

MANIFEST_PATH = Path(__file__).resolve().parents[1] / "agents" / "manifest.json"

WORKFLOWS = {
    "premium_home": [
        ("reference_audit", "direction_artistique", "DESIGN_CONTENT"),
        ("home_specification", "design_system", "FRONTEND_UI"),
        ("asset_integrity", "assets_hd", "ILLUSTRATION_MOTION"),
        ("wordpress_integration_plan", "wordpress_core", "WP_ARCHITECT"),
        ("responsive_fr_ar_qa", "responsive_fr_ar", "RESPONSIVE_MOBILE"),
        ("accessibility_qa", "accessibilite", "UX_ACCESSIBILITY"),
        ("performance_qa", "performance_seo", "PERFORMANCE_WP"),
        ("security_review", "securite", "SECURITY_PRIVACY"),
        ("release_review", "qualite_livraison", "QA_AUTOMATION"),
    ],
    "wordpress_feature": [
        ("wordpress_baseline_audit", "wordpress_core", "WP_ARCHITECT"),
        ("feature_architecture", "wordpress_core", "PHP_BACKEND"),
        ("data_privacy_review", "securite", "SECURITY_PRIVACY"),
        ("frontend_ui_spec", "design_system", "FRONTEND_UI"),
        ("responsive_fr_ar_qa", "responsive_fr_ar", "QA_LOCALIZATION"),
        ("security_review", "securite", "SECURITY_PRIVACY"),
        ("release_review", "qualite_livraison", "QA_AUTOMATION"),
    ],
    "asset_quality": [
        ("reference_audit", "direction_artistique", "DESIGN_CONTENT"),
        ("asset_integrity", "assets_hd", "ILLUSTRATION_MOTION"),
        ("resolution_dpr_review", "assets_hd", "PERFORMANCE_WP"),
        ("responsive_fr_ar_qa", "responsive_fr_ar", "RESPONSIVE_MOBILE"),
        ("release_review", "qualite_livraison", "QA_AUTOMATION"),
    ],
    "educational_module": [
        ("pedagogical_sources", "edtech_data", "CURRICULUM_MA"),
        ("learning_design", "edtech_data", "EDTECH"),
        ("localization", "responsive_fr_ar", "LOCALIZATION_FR_AR"),
        ("student_data_privacy", "securite", "LEGAL_EDTECH"),
        ("wordpress_integration_plan", "wordpress_core", "WP_ARCHITECT"),
        ("accessibility_qa", "accessibilite", "UX_ACCESSIBILITY"),
        ("release_review", "qualite_livraison", "QA_EDTECH_E2E"),
    ],
}

# External integrations must authenticate and apply action-specific permissions.
# These are just descriptions of the user's standing preferences.
AUTO_PREFERENCE = (
    "asset.list", "asset.verify", "mission.propose", "mission.read",
    "qa.preview", "qa.run_isolated", "dev.branch_write", "report.create",
)

def _indexed_manifest(manifest_path: Path = MANIFEST_PATH) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entities = {}
    entities[manifest["director"]["id"]] = (manifest["director"], None)
    for group, parent in (
        ("senior_managers", "director_id"),
        ("managers", "senior_manager_id"),
        ("team_leaders", "manager_id"),
        ("agents", "leader_id"),
    ):
        for obj in manifest[group]:
            if obj["id"] in entities:
                raise ValueError("Duplicate role ID")
            entities[obj["id"]] = (obj, obj[parent])
    for name, (_, parent) in entities.items():
        if parent and parent not in entities:
            raise ValueError("Missing reporting role for " + name)
    if len(entities) != 43:
        raise ValueError("Expected 43 documented roles")
    return entities


def _chain(role_id: str, roles: dict) -> list[dict]:
    current = role_id
    chain = []
    seen = set()
    while current is not None:
        if current in seen or current not in roles:
            raise ValueError("Cyclic or missing responsibility chain")
        seen.add(current)
        obj, current = roles[current]
        chain.append({"id": obj["id"], "name": obj["name"], "level": obj["level"]})
    if chain[-1]["id"] != "DSI":
        raise ValueError("Role must report to DSI")
    return list(reversed(chain))


def workforce_status(manifest_path: Path = MANIFEST_PATH) -> dict:
    indexed = _indexed_manifest(manifest_path)
    count = {"director": 0, "senior_manager": 0, "manager": 0, "team_leader": 0, "agent": 0}
    for obj, _ in indexed.values():
        count[obj["level"]] += 1
    return {
        "documented_roles": len(indexed),
        "by_level": count,
        "separate_running_agents_verified": 0,
        "orchestrator": "ChatGPT Pro standard (manual chat invocations only)",
        "surfaces_excluded": ["Work", "Codex"],
        "verification": "DOCUMENTATION_ONLY",
    }


def plan_enterprise_mission(kind: str, objective: str,
                            manifest_path: Path = MANIFEST_PATH) -> dict:
    if kind not in WORKFLOWS:
        raise ValueError("Unsupported mission type")
    if not isinstance(objective, str) or not (8 <= len(objective.strip()) <= 2500):
        raise ValueError("Objective must contain 8 to 2500 characters")
    roles = _indexed_manifest(manifest_path)
    steps = []
    for index, (name, module, lead) in enumerate(WORKFLOWS[kind], 1):
        if module not in MODULES or lead not in MODULES[module]["roles"]:
            raise ValueError("Workflow role and module registry conflict")
        chain = _chain(lead, roles)
        steps.append({
            "sequence": index,
            "step_id": name,
            "module": module,
            "responsibility": chain,
            "specialist": lead,
            "evidence_required": MODULES[module]["proofs"],
            "depends_on": steps[-1]["step_id"] if steps else None,
            "state": "NON TESTÉ",
            "evidence_collected": [],
            "executed": False,
        })
    return {
        "type": kind,
        "objective": objective.strip(),
        "project": "MNIN NBDA",
        "execution_surface": "ChatGPT standard — target Pro only",
        "work_codex_allowed": False,
        "execution_mode": "BLUEPRINT_ONLY",
        "live_agent_instances": 0,
        "all_stages": steps,
        "completion_gate": (
            "No PASS without real artifacts and observed tests. "
            "WordPress writes and public releases require separately verified approval."
        ),
        "cost_policy": {"paid_model_apis": False, "incremental_eur": 0},
    }


def subscription_gate_readiness() -> dict:
    """Static fail-closed declaration; NEVER validates a user's plan from a chat prompt."""
    return {
        "target_subscription": "ChatGPT Pro",
        "target_surface": "standard_chat_only",
        "excluded_surfaces": ["Work", "Codex"],
        "subscription_proof_received_from_trusted_identity_provider": False,
        "surface_proof_received_from_trusted_identity_provider": False,
        "strict_pro_only_server_gate_ready": False,
        "privileged_custom_mcp_writes_enabled": False,
        "conclusion": "BLOQUÉ",
        "reason": "No trusted subscription/surface attestation or remote OAuth server is implemented. "
                  "Client-provided plan flags are never trusted.",
    }
