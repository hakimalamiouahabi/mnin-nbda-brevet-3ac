#!/usr/bin/env python3
"""Lecture seule : cohérence du catalogue existant de 700 profils. Aucune API."""
from collections import Counter, defaultdict
from pathlib import Path
import json, sys

EXPECTED = {"dsi": 5, "senior_manager": 30, "manager": 60, "team_leader": 60, "expert": 545}
PARENT = {"dsi": None, "senior_manager": "dsi", "manager": "senior_manager",
          "team_leader": "manager", "expert": "team_leader"}

def audit(data):
    errors = []
    profiles = data.get("profiles", [])
    if not isinstance(profiles, list):
        return {"status": "FAIL", "errors": ["profiles n'est pas une liste"]}
    counts = Counter(p.get("level") for p in profiles if isinstance(p, dict))
    if dict(counts) != EXPECTED or data.get("counts") != EXPECTED or len(profiles) != 700:
        errors.append("Nombre de profils ou répartition non conforme au registre figé")
    identifiers = [p.get("id") for p in profiles if isinstance(p, dict)]
    if len(identifiers) != 700 or len(set(identifiers)) != 700:
        errors.append("Identifiants manquants ou dupliqués")
    by_id = {p["id"]: p for p in profiles if isinstance(p, dict) and p.get("id")}
    children = defaultdict(list)
    for p in profiles:
        if not isinstance(p, dict):
            errors.append("Profil malformé")
            continue
        rid, level, parent = p.get("id"), p.get("level"), p.get("parent_id")
        if not isinstance(rid, str) or not p.get("title"):
            errors.append("Identifiant ou intitulé manquant")
        target = PARENT.get(level, "INVALID")
        if target == "INVALID":
            errors.append(f"{rid}: niveau inconnu")
        elif target is None and parent != "OWNER":
            errors.append(f"{rid}: rattachement propriétaire absent")
        elif target is not None and (parent not in by_id or by_id[parent].get("level") != target):
            errors.append(f"{rid}: rattachement invalide: {parent}")
        children[parent].append(rid)
    for p in profiles:
        if not isinstance(p, dict):
            continue
        rid, level = p.get("id"), p.get("level")
        target_count = {"dsi": 6, "senior_manager": 2, "manager": 1}.get(level)
        if target_count is not None and len(children[rid]) != target_count:
            errors.append(f"{rid}: nombre de collaborateurs directs incorrect")
        if level == "team_leader" and len(children[rid]) not in (9, 10):
            errors.append(f"{rid}: doit coordonner 9 ou 10 experts")
    if data.get("status") != "TARGET_NOT_DEPLOYED":
        errors.append("Le catalogue ne doit pas être présenté comme déployé")
    return {"status": "FAIL" if errors else "PASS", "profiles": len(profiles),
            "counts": dict(counts), "unique_ids": len(set(identifiers)),
            "mode": "catalogue_non_deploye", "errors": errors[:50],
            "total_errors": len(errors)}

if __name__ == "__main__":
    try:
        path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("agents/manifest-700-target.json")
        result = audit(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError) as error:
        result = {"status": "FAIL", "errors": [str(error)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)
