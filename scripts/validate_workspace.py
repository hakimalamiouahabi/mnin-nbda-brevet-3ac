#!/usr/bin/env python3
"""Validation locale sans dépendances tierces du référentiel MNIN NBDA."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = [
    "AGENTS.md",
    "agents/01-pilotage.md",
    "agents/02-developpement.md",
    "agents/03-qualite.md",
    "agents/04-integration.md",
    "docs/references/PROMPT_MASTER_WORDPRESS_V4_2.md",
    "docs/references/PROMPT_MASTER_HOME_DESKTOP_XL_2026-10-11.md",
    "docs/WORK_MASTER_START.md",
    "docs/STATUS.md",
    "docs/ROADMAP.md",
]
errors = []
for rel in REQUIRED:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"Absent : {rel}")
    elif not path.read_text(encoding="utf-8").strip():
        errors.append(f"Vide : {rel}")

if shutil.which("php"):
    php_files = list(ROOT.rglob("*.php"))
    for path in php_files:
        result = subprocess.run(["php", "-l", str(path)], capture_output=True, text=True)
        if result.returncode:
            errors.append(f"PHP : {path.relative_to(ROOT)} : {result.stderr.strip()}")
    print(f"Contrôle syntaxique PHP : {len(php_files)} fichier(s)")
else:
    print("PHP non disponible : contrôle syntaxique PHP NON TESTÉ")

if errors:
    print("\n".join("ÉCHEC : " + err for err in errors), file=sys.stderr)
    sys.exit(1)
print("Référentiel : PASS (présence/non-vacuité)")
print("Installation WordPress, sécurité, responsive et parcours : NON TESTÉ")
