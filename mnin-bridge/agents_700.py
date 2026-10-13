"""700 documented MNIN NBDA roles: bounded, read-only organizational registry.

The 700 *profiles* are not 700 separately running AI models or API sessions.
A registry is useful for indexing expertise and delegating work through tools
actually connected to a normal ChatGPT conversation.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
import unicodedata

from premium_suite import MODULES

DEFAULT_FILE = Path(__file__).resolve().parents[1] / "agents" / "manifest-700-target.json"
EXPECTED_LEVELS = {"dsi": 5, "senior_manager": 30, "manager": 60, "team_leader": 60, "expert": 545}
LEVEL_PARENT = {
    "dsi": "OWNER", "senior_manager": "dsi", "manager": "senior_manager",
    "team_leader": "manager", "expert": "team_leader",
}
GROUP_MODULE = {
    "Direction artistique, marque et design premium": "direction_artistique",
    "Recherche UX et tests utilisateurs": "design_system",
    "Accessibilité et design inclusif": "accessibilite",
    "Illustration 2D et assets vectoriels": "assets_hd",
    "3D, animation et expérience WebGL": "assets_hd",
    "Interface responsive et localisation visuelle": "responsive_fr_ar",
    "Architecture WordPress et ingénierie PHP": "wordpress_core",
    "Backend et API métier": "wordpress_core",
    "Frontend HTML, CSS et JavaScript": "design_system",
    "Gestion des contenus et outils éditoriaux": "wordpress_core",
    "Performance Web et optimisation": "performance_seo",
    "QA logiciel, CI et déploiement": "qualite_livraison",
    "Référentiels officiels et programmes marocains": "edtech_data",
    "Ingénierie pédagogique et didactique": "edtech_data",
    "Mathématiques et raisonnement": "edtech_data",
    "Langues arabe, français et anglais": "edtech_data",
    "Sciences expérimentales et technologie": "edtech_data",
    "Histoire, géographie, civisme et autres disciplines": "edtech_data",
    "Data engineering et ingestion responsable": "edtech_data",
    "Architecture des données et gouvernance": "edtech_data",
    "Data analytics et tableaux de bord": "edtech_data",
    "Data science et évaluation de l'apprentissage": "edtech_data",
    "AI engineering local et modèles accessibles": "edtech_data",
    "Personnalisation explicable et moteur de règles": "edtech_data",
    "Cybersécurité applicative et contrôle d'accès": "securite",
    "Données des mineurs, vie privée et conformité": "securite",
    "Direction produit, PMO et exécution": "qualite_livraison",
    "SEO, recherche et croissance responsable": "performance_seo",
    "Accompagnement élèves, parents et communauté": "edtech_data",
    "FinOps, observabilité et continuité": "qualite_livraison",
}
ID_FORMAT = re.compile(r"^(DSI|SM|MGR|TL|EX)_[A-Za-z0-9_]+$")
MODULE_BY_ID = frozenset(MODULES)

def _tokens(value: str) -> frozenset[str]:
    normalized = "".join(c for c in unicodedata.normalize("NFKD", value.casefold())
                         if not unicodedata.combining(c))
    return frozenset(t for t in re.findall(r"[a-z0-9]{3,}", normalized)
                     if t not in {"des", "les", "dans", "pour", "avec", "une", "aux",
                                  "expert", "experts", "manager", "agents", "agent"})


def _registry(manifest_path: Path = DEFAULT_FILE) -> tuple[dict, dict]:
    if not manifest_path.is_file():
        raise FileNotFoundError("700-profile proposal manifest is unavailable")
    doc = json.loads(manifest_path.read_text(encoding="utf-8"))
    if doc.get("schema_version") != "proposal-1" or doc.get("status") != "TARGET_NOT_DEPLOYED":
        raise ValueError("Untrusted or misrepresented agent manifest")
    profiles = doc.get("profiles")
    if not isinstance(profiles, list) or len(profiles) != 700:
        raise ValueError("Exactly 700 documented profiles required")
    by_id = {}
    counts = Counter()
    actual_groups = set()
    for item in profiles:
        if not isinstance(item, dict):
            raise ValueError("Invalid profile record")
        pid, level, title, parent = (item.get(k) for k in ("id", "level", "title", "parent_id"))
        if not isinstance(pid, str) or not ID_FORMAT.fullmatch(pid) or pid in by_id:
            raise ValueError("Invalid or duplicate profile ID")
        if level not in EXPECTED_LEVELS or not isinstance(title, str) or not title.strip():
            raise ValueError("Invalid profile level/title")
        if not isinstance(parent, str):
            raise ValueError("Invalid reporting parent")
        by_id[pid] = item
        counts[level] += 1
        if level == "expert":
            if item.get("state") != "catalogued_not_running":
                raise ValueError("An expert profile is misrepresented as active")
            group = item.get("competency_group")
            if not isinstance(group, str) or group not in GROUP_MODULE:
                raise ValueError("Unknown expert competency group")
            actual_groups.add(group)
    if dict(counts) != EXPECTED_LEVELS or dict(doc.get("counts", {})) != EXPECTED_LEVELS:
        raise ValueError("Manifest role counts mismatch")
    if actual_groups != set(GROUP_MODULE):
        raise ValueError("Competency group coverage mismatch")
    for pid, item in by_id.items():
        level, parent = item["level"], item["parent_id"]
        if level == "dsi":
            if parent != "OWNER":
                raise ValueError("Only owner may supervise a DSI profile")
        elif parent not in by_id or by_id[parent]["level"] != LEVEL_PARENT[level]:
            raise ValueError("Broken role reporting hierarchy")
    return doc, by_id


def _path(pid: str, profiles: dict) -> list[dict]:
    if pid not in profiles:
        raise ValueError("Unknown role")
    out, seen = [], set()
    while pid != "OWNER":
        if pid in seen or pid not in profiles:
            raise ValueError("Invalid reporting chain")
        seen.add(pid)
        item = profiles[pid]
        out.append({"id": item["id"], "level": item["level"], "title": item["title"]})
        pid = item["parent_id"]
    return [{"id": "OWNER", "level": "owner", "title": "Arbitrage du propriétaire"}] + list(reversed(out))


def registry_700_status(manifest_path: Path = DEFAULT_FILE) -> dict:
    manifest, by_id = _registry(manifest_path)
    by_module = Counter(GROUP_MODULE[p["competency_group"]] for p in by_id.values()
                        if p["level"] == "expert")
    return {
        "version": "0.9.0",
        "documented_profiles": len(by_id),
        "distribution": EXPECTED_LEVELS.copy(),
        "directorate_profiles": [{"id": x["id"], "title": x["title"]}
                                  for x in by_id.values() if x["level"] == "dsi"],
        "specialist_groups": len(GROUP_MODULE),
        "experts_assigned_to_modules": sum(by_module.values()),
        "expert_coverage_by_module": {key: by_module[key] for key in MODULES},
        "running_autonomous_agents_verified": 0,
        "runtime": "PROFILE_REGISTRY_ONLY",
        "status": manifest["status"],
        "standing_permissions_do_not_spawn_agents": True,
        "requires_work_or_codex": False,
        "paid_ai_api_budget": 0,
    }


def search_agent_700(objective: str, module: str = "",
                     limit: int = 8, manifest_path: Path = DEFAULT_FILE) -> dict:
    if not isinstance(objective, str) or not (3 <= len(objective.strip()) <= 500):
        raise ValueError("Search objective must be 3..500 characters")
    if not isinstance(module, str) or (module and module not in MODULE_BY_ID):
        raise ValueError("Unknown module")
    if type(limit) is not int or limit not in range(1, 21):
        raise ValueError("Profile search limit must be 1..20")
    _, by_id = _registry(manifest_path)
    query = _tokens(objective)
    ranked = []
    for profile in by_id.values():
        if profile["level"] != "expert":
            continue
        group = profile["competency_group"]
        linked_module = GROUP_MODULE[group]
        if module and linked_module != module:
            continue
        title_tokens = _tokens(profile["title"])
        group_tokens = _tokens(group)
        match = (len(query & title_tokens) * 5 + len(query & group_tokens) * 2)
        if not match and not module:
            continue
        ranked.append((match, profile["id"], profile, linked_module))
    ranked.sort(key=lambda p: (-p[0], p[1]))
    return {
        "objective": objective.strip(),
        "selected_module": module or None,
        "total_matched": len(ranked),
        "profiles": [
            {
                "id": p["id"], "title": p["title"], "competency_group": p["competency_group"],
                "module": linked_module, "score": score,
                "responsibility_chain": _path(p["id"], by_id),
                "execution_state": "CATALOGUED_NOT_RUNNING",
                "actions_performed": 0,
            } for score, _, p, linked_module in ranked[:limit]
        ],
        "mode": "READ_ONLY_PLAN",
        "autonomous_instances_started": 0,
    }


def plan_700_mission(objective: str, modules: list[str],
                     manifest_path: Path = DEFAULT_FILE) -> dict:
    if not isinstance(modules, list) or not (1 <= len(modules) <= 10):
        raise ValueError("Select 1..10 modules")
    if any(not isinstance(m, str) or m not in MODULES for m in modules):
        raise ValueError("Invalid module")
    if len(set(modules)) != len(modules):
        raise ValueError("Repeated modules")
    _, by_id = _registry(manifest_path)
    steps = []
    for i, m in enumerate(modules, 1):
        result = search_agent_700(objective, m, 2, manifest_path)
        if not result["profiles"]:
            raise RuntimeError("No expert profile assigned to " + m)
        steps.append({
            "sequence": i, "module": m, "label": MODULES[m]["label"],
            "profiles": result["profiles"], "evidence_required": MODULES[m]["proofs"],
            "depends_on": steps[-1]["module"] if steps else None,
            "execution_status": "NON TESTÉ", "actions_performed": 0,
        })
    return {
        "objective": objective.strip(), "steps": steps,
        "management": "5 DSI profiles under owner; 700 role definitions",
        "profiles_catalogued": len(by_id), "running_agents_verified": 0,
        "execution": "BLUEPRINT_NOT_STARTED",
        "permissions": "Provider/OAuth permissions and approvals checked separately for real actions",
        "chatgpt_surface": "STANDARD_CHAT_ONLY_TARGET_PRO_UNATTESTED",
        "requires_work_or_codex": False, "paid_ai_api_calls": 0,
    }
