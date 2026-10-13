#!/usr/bin/env python3
"""Route des missions vers les IDENTIFIANTS EXISTANTS, sans créer d'agent ni appeler une API."""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

STOPWORDS = {"pour", "dans", "avec", "sans", "une", "des", "les", "sur", "the", "and", "de", "du", "une", "et", "aux"}

def tokens(value):
    simplified = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode().lower()
    return {word for word in re.findall(r"[a-z0-9]+", simplified) if len(word) >= 3 and word not in STOPWORDS}

def route(catalog, mission, count=5, role_id=None):
    profiles = catalog["profiles"]
    index = {p["id"]: p for p in profiles}
    if role_id:
        if role_id not in index:
            raise ValueError("Identifiant inexistant dans le registre 700")
        chosen = [index[role_id]]
    else:
        wanted = tokens(mission)
        if not wanted:
            raise ValueError("Mission insuffisamment explicite")
        scored = []
        for p in profiles:
            if p["level"] != "expert":
                continue
            title_match = len(wanted & tokens(p.get("title", "")))
            group_match = len(wanted & tokens(p.get("competency_group", "")))
            score = 3 * title_match + group_match
            if score:
                scored.append((score, p["id"], p))
        scored.sort(key=lambda x: (-x[0], x[1]))
        chosen = [p for _, _, p in scored[:count]]
    assignments = []
    for role in chosen:
        ancestors, current, visited = [], role, set()
        while current.get("parent_id") not in (None, "OWNER"):
            if current["id"] in visited:
                raise ValueError("Cycle hierarchique dans le registre")
            visited.add(current["id"])
            current = index.get(current["parent_id"])
            if not current:
                raise ValueError("Parent introuvable dans le registre")
            ancestors.insert(0, {"id": current["id"], "title": current["title"]})
        assignments.append({"id": role["id"], "title": role["title"],
                            "chain": ancestors + [{"id": role["id"], "title": role["title"]}],
                            "status": "ROLE_ASSIGNE_NON_EXECUTE"})
    return {"mission": mission, "selected": len(assignments),
            "source_profiles": len(profiles), "inference_started": False,
            "no_new_agents": True, "assignments": assignments}

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--mission", required=True)
    cli.add_argument("--manifest", default="agents/manifest-700-target.json")
    cli.add_argument("--role-id", default=None)
    cli.add_argument("--count", type=int, default=5)
    args = cli.parse_args()
    try:
        if not 1 <= args.count <= 30:
            raise ValueError("count doit être compris entre 1 et 30")
        j = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        print(json.dumps(route(j, args.mission, args.count, args.role_id), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
