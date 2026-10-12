"""MNIN Bridge Pro v0.4 — deterministic premium-site planning for ChatGPT Pro.

NO code execution, agents, WordPress mutation, token issuance or cost commitment.
The LLM may interpret tasks; this module only validates and structures plans.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

DEFAULT_POLICY = Path(__file__).with_name("owner_delegation_policy.json")

MODULES = {
    "direction_artistique": {
        "label": "Direction artistique premium",
        "roles": ["DESIGN_CONTENT", "ILLUSTRATION_MOTION"],
        "keywords": ["maquette", "design", "graphisme", "premium", "illustration", "branding", "visuel", "charte"],
        "proofs": ["Référence visuelle approuvée identifiée", "Écarts documentés sans invention"],
    },
    "design_system": {
        "label": "Design system et composants",
        "roles": ["FRONTEND_UI", "UX_ACCESSIBILITY"],
        "keywords": ["composant", "bouton", "typo", "police", "palette", "espacement", "tokens", "ui"],
        "proofs": ["Inventaire de composants", "États interactifs et contrastes vérifiables"],
    },
    "wordpress_core": {
        "label": "Architecture WordPress thème et plugin",
        "roles": ["WP_ARCHITECT", "PHP_BACKEND", "WEB_DEV"],
        "keywords": ["wordpress", "plugin", "extension", "thème", "theme", "php", "gutenberg", "api"],
        "proofs": ["Séparation thème / logique métier", "Contrôles d'accès et nonces vérifiés"],
    },
    "responsive_fr_ar": {
        "label": "Responsive, français et arabe RTL",
        "roles": ["RESPONSIVE_MOBILE", "LOCALIZATION_FR_AR", "QA_LOCALIZATION"],
        "keywords": ["responsive", "mobile", "tablette", "darija", "arabe", "rtl", "français", "ecran"],
        "proofs": ["Captures multi-viewport", "Vérification de la direction RTL et du texte"],
    },
    "assets_hd": {
        "label": "Assets, SVG et haute résolution",
        "roles": ["ILLUSTRATION_MOTION", "DESIGN_CONTENT", "PERFORMANCE_WP"],
        "keywords": ["8k", "pixel", "résolution", "svg", "image", "logo", "icone", "icône", "webp"],
        "proofs": ["Dimension intrinsèque et hash des originaux", "Dimension d'affichage et densité adaptées"],
    },
    "edtech_data": {
        "label": "Ingénierie pédagogique et données",
        "roles": ["EDTECH", "CURRICULUM_MA", "DATA_ENG", "DATA_GOVERNANCE"],
        "keywords": ["eleve", "élève", "parent", "exercice", "quiz", "progression", "cours", "data"],
        "proofs": ["Périmètre pédagogique explicite", "Données personnelles des mineurs exclues des tests"],
    },
    "accessibilite": {
        "label": "Accessibilité et inclusion",
        "roles": ["UX_ACCESSIBILITY", "QA_LOCALIZATION"],
        "keywords": ["accessibilité", "wcag", "contraste", "clavier", "lecteur", "inclusion"],
        "proofs": ["Contrôles clavier et focus", "Résultats de tests documentés, sans fausse certification"],
    },
    "performance_seo": {
        "label": "Performance web et SEO",
        "roles": ["PERFORMANCE_WP", "SEO_GROWTH"],
        "keywords": ["performance", "lighthouse", "seo", "vitesse", "core web vitals", "cache", "optimisation"],
        "proofs": ["Mesures datées dans un environnement identifié", "Aucun score présumé"],
    },
    "securite": {
        "label": "Cybersécurité et confidentialité",
        "roles": ["SECURITY_PRIVACY", "LEGAL_EDTECH"],
        "keywords": ["sécurité", "authentification", "confidentialité", "rgpd", "permission", "audit"],
        "proofs": ["Droits minimaux et journal d'accès", "Aucun secret ou donnée d'élève en dépôt public"],
    },
    "qualite_livraison": {
        "label": "Tests et livraison contrôlée",
        "roles": ["QA_AUTOMATION", "QA_EDTECH_E2E", "DEVOPS", "OBSERVABILITY"],
        "keywords": ["test", "qa", "livraison", "bug", "release", "déploiement", "validation"],
        "proofs": ["Résultats de tests réellement exécutés", "Retour arrière et approbations vérifiés"],
    },
}

ORDER = tuple(MODULES)
STANDING = frozenset({
    "asset.list", "asset.verify", "mission.propose", "mission.read",
    "qa.preview", "qa.run_isolated", "dev.branch_write", "report.create",
    "source.read", "source.compare", "branch.create", "git.pr_draft",
    "qa.static_review", "design.propose", "docs.update_branch",
    "skills.read", "requirements.analyze", "performance.plan", "accessibility.plan",
})
PER_ACTION = frozenset({
    "wordpress.staging_write", "wordpress.production_write", "github.merge_to_main",
    "github.repo_settings", "hosting.deploy_public", "hosting.change_plan",
    "billing.create_resource", "billing.charge", "data.export_private",
    "secrets.create_or_rotate", "secrets.export", "domain.dns_change",
    "permissions.change", "mass_delete", "workflow.activate_recurring",
})
CRITICAL = frozenset({
    "secrets.export", "child_data.export", "disable_security_logging",
    "unrestricted_shell", "unbounded_agent_execution",
})

def module_catalog() -> dict:
    return {
        "version": "0.4.0",
        "modules": [{"id": key, "label": value["label"], "roles": value["roles"],
                     "proofs": value["proofs"]} for key, value in MODULES.items()],
        "module_count": len(MODULES),
        "execution": "PLAN_ONLY",
        "agents_actually_started": 0,
    }

def propose_premium_plan(task: str, selected: list[str] | None = None) -> dict:
    if not isinstance(task, str) or not (4 <= len(task.strip()) <= 2000):
        raise ValueError("task must be 4 to 2000 characters")
    if selected is not None and (
        not isinstance(selected, list)
        or len(selected) > len(MODULES)
        or any(not isinstance(k, str) or k not in MODULES for k in selected)
    ):
        raise ValueError("Unknown module or oversized module selection")
    if selected is None:
        lower = task.lower()
        selected = [key for key, item in MODULES.items()
                    if any(re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", lower)
                           for term in item["keywords"])]
        if not selected:
            selected = ["direction_artistique", "wordpress_core", "qualite_livraison"]
    keys = [k for k in ORDER if k in set(selected)]
    return {
        "task": task.strip(), "selected_modules": keys,
        "project": "MNIN NBDA",
        "governance": "DSI > Senior Manager > Manager > Team Leader > expert",
        "steps": [{"module": k, "purpose": MODULES[k]["label"],
                   "roles_requested": MODULES[k]["roles"],
                   "acceptance_evidence": MODULES[k]["proofs"],
                   "roles_spawned": 0, "status": "PLAN_ONLY"}
                  for k in keys],
        "nonnegotiable": [
            "ChatGPT standard, sans Work ni Codex",
            "Aucune API IA payante ni coût supplémentaire",
            "Aucune écriture WordPress, publication ou DNS sans approbation distincte",
            "Aucune donnée de mineurs ni secret dans le dépôt GitHub public",
            "Comparaison aux références validées uniquement",
            "Tests rapportés PASS / FAIL / NON TESTÉ / BLOQUÉ sans inventer d'exécution",
        ],
        "effect": "NO REMOTE ACTION PERFORMED",
    }

def delegation_status(action: str, policy_path: str | Path = DEFAULT_POLICY) -> dict:
    """Explain owner standing instructions, NEVER authenticate or authorize an action."""
    if not isinstance(action, str) or len(action) > 120:
        raise ValueError("Invalid action")
    policy = json.loads(Path(policy_path).read_text(encoding="utf-8"))
    delegation = policy["standing_delegation"]
    if action in CRITICAL:
        category = "BLOCK_WITHOUT_SEPARATE_CAPABILITY"
    elif action in PER_ACTION:
        category = "EXPLICIT_PER_ACTION_APPROVAL"
    elif action in STANDING and action in delegation.get("allow_without_reprompt", []):
        category = "STANDING_INSTRUCTION"
    else:
        category = "NOT_ALLOWED"
    return {
        "action": action,
        "classification": category,
        "owner_standing_instruction": bool(delegation.get("enabled"))
            and category == "STANDING_INSTRUCTION",
        "policy_status": policy["status"],
        "trusted_identity_verified": False,
        "chatgpt_pro_entitlement_verified": False,
        "chat_surface_verified": False,
        "runtime_execution_authorized": False,
        "reason": "Standing consent is a preference, not OAuth or runtime capability. "
                  "Provider-side permissions and action-specific approvals remain required.",
    }
