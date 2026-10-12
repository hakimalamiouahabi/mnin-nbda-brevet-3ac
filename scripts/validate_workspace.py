#!/usr/bin/env python3
"""Contrôle statique sans API ni paquet Python tiers du référentiel MNIN NBDA."""
from __future__ import annotations
from pathlib import Path
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
AGENT_FILES = [
    "agents/01-directeur-si.md",
    "agents/02-data-engineering.md",
    "agents/03-data-science.md",
    "agents/04-data-analyst.md",
    "agents/05-ia-engineering.md",
    "agents/06-developpement-web.md",
    "agents/07-design-content.md",
    "agents/08-devops.md",
]
REQUIRED = [
    "README.md", "AGENTS.md", "agents/manifest.json",
    "docs/AGENT_OPERATING_MODEL.md",
    "docs/WORK_MASTER_START.md", "docs/ROADMAP.md", "docs/STATUS.md",
    "docs/references/PROMPT_MASTER_WORDPRESS_V4_2.md",
    "docs/references/PROMPT_MASTER_HOME_DESKTOP_XL_2026-10-11.md",
    *AGENT_FILES,
]
errors = []
for rel in REQUIRED:
    p = ROOT / rel
    if not p.is_file():
        errors.append(f"Fichier obligatoire absent : {rel}")
    elif not p.read_text(encoding="utf-8").strip():
        errors.append(f"Fichier vide : {rel}")

manifest_path = ROOT / "agents/manifest.json"
if manifest_path.is_file():
    try:
        m = json.loads(manifest_path.read_text(encoding="utf-8"))
        agents = m["agents"]
        ids = [a["id"] for a in agents]
        paths = [a["file"] for a in agents]
        if len(agents) != 8 or len(set(ids)) != 8 or len(set(paths)) != 8:
            errors.append("Manifest : il doit contenir exactement 8 identifiants et fichiers uniques")
        if set(paths) != set(AGENT_FILES):
            errors.append("Manifest : la liste de fichiers ne correspond pas aux 8 rôles attendus")
        if m.get("policy", {}).get("paid_ai_api") is not False:
            errors.append("Manifest : interdiction des API IA payantes manquante")
        if m.get("policy", {}).get("production_deploy_requires_approval") is not True:
            errors.append("Manifest : déploiement sans autorisation possible")
        for entry in agents:
            if not entry.get("outputs"):
                errors.append(f"Manifest : aucun livrable pour {entry.get('id')}")
    except (ValueError, KeyError, TypeError) as exc:
        errors.append(f"Manifest JSON invalide : {exc}")

for obsolete in [
    "agents/01-pilotage.md", "agents/02-developpement.md",
    "agents/03-qualite.md", "agents/04-integration.md",
]:
    if (ROOT / obsolete).exists():
        errors.append(f"Ancien profil conflictuel encore présent : {obsolete}")

php = shutil.which("php")
if php:
    php_files = sorted(ROOT.rglob("*.php"))
    for file in php_files:
        result = subprocess.run(
            [php, "-l", str(file)], capture_output=True, text=True, check=False,
        )
        if result.returncode:
            errors.append(f"Syntaxe PHP : {file.relative_to(ROOT)} : {result.stderr.strip()}")
    print(f"Syntaxe PHP : {len(php_files)} fichier(s) contrôlé(s)")
else:
    print("Syntaxe PHP : NON TESTÉ (binaire PHP indisponible)")

if errors:
    for err in errors:
        print("FAIL : " + err, file=sys.stderr)
    sys.exit(1)

print("PASS : fichiers requis présents et non vides")
print("PASS : 8 agents distincts et manifest cohérent")
print("NON TESTÉ : fonctionnement indépendant ou continu des agents Work/Codex")
print("NON TESTÉ : installation WordPress, UX responsive, protection des mineurs et recette")
