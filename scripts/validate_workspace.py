#!/usr/bin/env python3
"""Vérification locale de la hiérarchie MNIN NBDA — sans API ni dépendances Python externes."""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = [
    "README.md", "AGENTS.md", "docs/AGENT_OPERATING_MODEL.md",
    "docs/WORK_MASTER_START.md", "docs/ROADMAP.md", "docs/STATUS.md",
    "docs/references/PROMPT_MASTER_WORDPRESS_V4_2.md",
    "docs/references/PROMPT_MASTER_HOME_DESKTOP_XL_2026-10-11.md",
    "agents/manifest.json", "agents/org-structure.json",
]
errors = []

def assert_file(rel: str) -> None:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"Manquant : {rel}")
    elif not path.read_text(encoding="utf-8").strip():
        errors.append(f"Vide : {rel}")

for rel in REQUIRED:
    assert_file(rel)

manifest_file = ROOT / "agents/manifest.json"
if manifest_file.is_file():
    try:
        m = json.loads(manifest_file.read_text(encoding="utf-8"))
        director = m["director"]
        seniors = m["senior_managers"]
        managers = m["managers"]
        leads = m["team_leaders"]
        agents = m["agents"]
        expected = {
            "director": 1, "senior_managers": 3, "managers": 3,
            "team_leaders": 6, "specialist_agents": 30, "total_profiles": 43,
        }
        if m.get("counts") != expected:
            errors.append("Décompte déclaré non conforme : 1+3+3+6+30=43 requis")
        groups = [director, *seniors, *managers, *leads, *agents]
        if len(seniors) != 3 or len(managers) != 3 or len(leads) != 6 or len(agents) != 30:
            errors.append("Nombre réel de profils incohérent avec la hiérarchie")
        ids = [p["id"] for p in groups]
        files = [p["file"] for p in groups]
        if len(groups) != 43 or len(set(ids)) != 43 or len(set(files)) != 43:
            errors.append("Profils ou chemins en doublon")
        for rel in files:
            assert_file(rel)
        if director["id"] != "DSI":
            errors.append("La racine de l'organigramme doit être le DSI")
        senior_ids = {p["id"] for p in seniors}
        manager_ids = {p["id"] for p in managers}
        lead_ids = {p["id"] for p in leads}
        if not all(p.get("director_id") == "DSI" for p in seniors):
            errors.append("Un Senior Manager n'est pas rattaché au DSI")
        if not all(p.get("senior_manager_id") in senior_ids for p in managers):
            errors.append("Un Manager sans Senior Manager valide")
        if not all(p.get("manager_id") in manager_ids for p in leads):
            errors.append("Un Team Leader sans Manager valide")
        if not all(p.get("leader_id") in lead_ids for p in agents):
            errors.append("Un agent expert sans Team Leader valide")
        per_senior = Counter(p["senior_manager_id"] for p in managers)
        per_manager = Counter(p["manager_id"] for p in leads)
        per_lead = Counter(p["leader_id"] for p in agents)
        if any(per_senior[x] != 1 for x in senior_ids):
            errors.append("Chaque Senior Manager doit superviser exactement 1 Manager")
        if any(per_manager[x] != 2 for x in manager_ids):
            errors.append("Chaque Manager doit superviser exactement 2 Team Leaders")
        if any(per_lead[x] != 5 for x in lead_ids):
            errors.append("Chaque Team Leader doit encadrer exactement 5 experts")
        policy = m.get("policy", {})
        if policy.get("paid_ai_api") is not False:
            errors.append("Interdiction des API IA payantes absente")
        if policy.get("production_deploy_requires_approval") is not True:
            errors.append("Validation humaine avant déploiement absente")

        tree_file = ROOT / "agents/org-structure.json"
        if tree_file.is_file():
            tree = json.loads(tree_file.read_text(encoding="utf-8"))
            if tree.get("counts") != expected:
                errors.append("Décompte de l'organigramme imbriqué incohérent")
            branches = tree["director"]["senior_managers"]
            if len(branches) != 3:
                errors.append("L'arbre doit présenter 3 branches Senior Manager")
            nested_seniors = {s["id"] for s in branches}
            nested_managers = [mgr for s in branches for mgr in s["manager"]]
            nested_leads = [lead for mgr in nested_managers for lead in mgr["team_leaders"]]
            nested_agents = [a for lead in nested_leads for a in lead["agents"]]
            if (nested_seniors != senior_ids
                    or {p["id"] for p in nested_managers} != manager_ids
                    or {p["id"] for p in nested_leads} != lead_ids
                    or {p["id"] for p in nested_agents} != {p["id"] for p in agents}):
                errors.append("L'arbre et le manifest ne référencent pas les mêmes profils")
            if not all(len(mgr["team_leaders"]) == 2 for mgr in nested_managers):
                errors.append("Arbre : Manager avec nombre incorrect de Team Leaders")
            if not all(len(lead["agents"]) == 5 for lead in nested_leads):
                errors.append("Arbre : équipe sans exactement 5 spécialistes")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as ex:
        errors.append(f"Manifest ou organigramme invalide : {ex}")

for obsolete in ["agents/01-pilotage.md", "agents/02-developpement.md",
                 "agents/03-qualite.md", "agents/04-integration.md"]:
    if (ROOT / obsolete).exists():
        errors.append(f"Ancien profil de l'organisation 4 agents encore présent : {obsolete}")

php = shutil.which("php")
php_files = sorted(ROOT.rglob("*.php"))
if php and php_files:
    for f in php_files:
        p = subprocess.run([php, "-l", str(f)], capture_output=True, text=True, check=False)
        if p.returncode:
            errors.append(f"Syntaxe PHP : {f.relative_to(ROOT)} : {p.stderr.strip()}")
    print(f"PHP lint : {len(php_files)} fichier(s)")
else:
    print("PHP lint : NON TESTÉ (PHP indisponible ou aucun code PHP dans le dépôt)")

if errors:
    for error in errors:
        print("FAIL : " + error, file=sys.stderr)
    sys.exit(1)

print("PASS : 43 définitions uniques et complètes")
print("PASS : chaîne DSI > 3 Senior Managers > 3 Managers > 6 Team Leaders > 30 experts")
print("PASS : 6 équipes contenant exactement 5 spécialistes")
print("PASS : conformité du manifest et de l'organigramme")
print("NON TESTÉ : exécution autonome Work/Codex, site WordPress et tests fonctionnels")
