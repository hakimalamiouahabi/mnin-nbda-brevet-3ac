#!/usr/bin/env python3
"""Select ONLY existing MNIN roles for one ChatGPT conversation.

Pure Python, no AI API or remote calls. Returning a role is not running an agent.
"""
import argparse
from collections import Counter
import json
import re
import sys
import unicodedata
from pathlib import Path

EXPECTED = {"dsi": 5, "senior_manager": 30, "manager": 60, "team_leader": 60, "expert": 545}
PARENT_LEVEL = {"senior_manager": "dsi", "manager": "senior_manager",
                "team_leader": "manager", "expert": "team_leader"}
STOPWORDS = {"pour", "dans", "avec", "sans", "une", "des", "les", "sur",
             "the", "and", "de", "du", "et", "aux", "mon", "mes", "ma", "ton",
             "notre", "outil", "equipe", "experts", "expert", "agent", "agents"}
# These aliases point to EXISTING competency groups in the immutable manifest.
# They do not invent an expert or grant professional credentials.
INTENTS = (
    ({"wordpress", "site", "theme", "plugin", "home", "accueil", "page"},
     ("Architecture WordPress et ingénierie PHP", "Frontend HTML, CSS et JavaScript",
      "QA logiciel, CI et déploiement", "Performance Web et optimisation")),
    ({"bug", "bugs", "panne", "reparer", "corriger", "marche", "fonctionne",
      "fonctionnement", "echec", "bloque", "casse", "erreur", "incident"},
     ("QA logiciel, CI et déploiement", "Backend et API métier",
      "Cybersécurité applicative et contrôle d'accès", "Performance Web et optimisation")),
    ({"github", "depot", "branche", "commit", "ci", "tests", "workflow", "pipeline"},
     ("QA logiciel, CI et déploiement", "Backend et API métier")),
    ({"cloudflare", "d1", "bdd", "sql", "database", "donnees", "base"},
     ("Architecture des données et gouvernance", "Data engineering et ingestion responsable",
      "Cybersécurité applicative et contrôle d'accès")),
    ({"design", "maquette", "graphisme", "visuel", "illustration"},
     ("Direction artistique, marque et design premium",
      "Illustration 2D et assets vectoriels", "Recherche UX et tests utilisateurs")),
    ({"mobile", "responsive", "arabe", "rtl", "francais", "accessibilite"},
     ("Interface responsive et localisation visuelle", "Accessibilité et design inclusif")),
    ({"pedagogie", "ecole", "eleves", "exercices", "mathematiques", "cours"},
     ("Ingénierie pédagogique et didactique", "Mathématiques et raisonnement",
      "Référentiels officiels et programmes marocains")),
)


def tokens(value):
    if not isinstance(value, str):
        raise ValueError("La mission doit être du texte")
    simplified = "".join(ch for ch in unicodedata.normalize("NFKD", value.casefold())
                         if not unicodedata.combining(ch))
    return {word for word in re.findall(r"[a-z0-9]+", simplified)
            if len(word) >= 3 and word not in STOPWORDS}


def _index(catalog):
    if not isinstance(catalog, dict) or catalog.get("status") != "TARGET_NOT_DEPLOYED":
        raise ValueError("Catalogue d'origine absent ou statut non vérifié")
    profiles = catalog.get("profiles")
    if not isinstance(profiles, list) or len(profiles) != 700:
        raise ValueError("Le registre doit contenir exactement 700 profils")
    if catalog.get("counts") != EXPECTED:
        raise ValueError("Les effectifs des 700 profils ont changé")
    if any(not isinstance(p, dict) or not isinstance(p.get("id"), str) or
           not isinstance(p.get("title"), str) or not p["title"].strip()
           for p in profiles):
        raise ValueError("Fiche invalide")
    ids = [p["id"] for p in profiles]
    if len(set(ids)) != 700:
        raise ValueError("Identifiants manquants ou dupliqués")
    by_id = {p["id"]: p for p in profiles}
    if Counter(p.get("level") for p in profiles) != EXPECTED:
        raise ValueError("Hiérarchie des 700 profils non conforme")
    for p in profiles:
        level, parent = p["level"], p.get("parent_id")
        if level == "dsi":
            if parent != "OWNER":
                raise ValueError("Directeur mal rattaché")
        elif parent not in by_id or by_id[parent]["level"] != PARENT_LEVEL[level]:
            raise ValueError("Rattachement de profil invalide")
        if level == "expert" and p.get("state") != "catalogued_not_running":
            raise ValueError("Aucune instance d'expert active ne peut être inventée")
    return profiles, by_id


def _chain(profile, index):
    chain, current, seen = [], profile, set()
    while current.get("parent_id") != "OWNER":
        if current["id"] in seen:
            raise ValueError("Hiérarchie cyclique")
        seen.add(current["id"])
        chain.insert(0, {"id": current["id"], "title": current["title"]})
        current = index[current["parent_id"]]
    chain.insert(0, {"id": current["id"], "title": current["title"]})
    return chain


def route(catalog, mission, count=5, role_id=None):
    profiles, index = _index(catalog)
    if not isinstance(mission, str) or not (3 <= len(mission.strip()) <= 600):
        raise ValueError("Mission vide, trop courte ou trop longue")
    if type(count) is not int or not (1 <= count <= 30):
        raise ValueError("count doit être compris entre 1 et 30")
    if role_id is not None:
        if role_id not in index:
            raise ValueError("Identifiant inexistant dans les 700 profils")
        chosen = [index[role_id]]
    else:
        wanted = tokens(mission)
        if not wanted:
            raise ValueError("Préciser la mission à effectuer")
        domain_boost = {}
        for triggers, groups in INTENTS:
            if wanted & triggers:
                for i, group in enumerate(groups):
                    domain_boost[group] = max(domain_boost.get(group, 0), 12 - i)
        ranked = []
        for p in profiles:
            if p["level"] != "expert":
                continue
            title_tokens = tokens(p.get("title", ""))
            group = p.get("competency_group", "")
            score = (5 * len(title_tokens & wanted) +
                     2 * len(tokens(group) & wanted) +
                     domain_boost.get(group, 0))
            if score:
                ranked.append((score, p["id"], p))
        ranked.sort(key=lambda e: (-e[0], e[1]))
        # Prefer distinct documented professions and complementary specialisms.
        chosen, selected_groups, selected_titles, selected_ids = [], set(), set(), set()
        for pass_number in (0, 1, 2):
            for _, _, p in ranked:
                if len(chosen) >= count:
                    break
                if p["id"] in selected_ids:
                    continue
                title_key = tokens(p["title"])
                if pass_number == 0 and p.get("competency_group") in selected_groups:
                    continue
                if pass_number == 1 and title_key in selected_titles:
                    continue
                chosen.append(p)
                selected_ids.add(p["id"])
                selected_groups.add(p.get("competency_group"))
                selected_titles.add(title_key)
            if len(chosen) >= count:
                break
    assignments = [
        {"id": p["id"], "title": p["title"],
         "competency_group": p.get("competency_group"),
         "chain": _chain(p, index), "status": "ROLE_ASSIGNE_NON_EXECUTE"}
        for p in chosen
    ]
    return {
        "mission": mission.strip(), "status": "ROUTAGE_PRET" if chosen else "AUCUN_PROFIL_IDENTIFIE",
        "selected": len(assignments), "source_profiles": 700,
        "inference_started": False, "autonomous_agents_started": 0,
        "no_new_agents": True, "assignments": assignments,
        "message": ("Analyse possible dans le chat; aucun agent autonome démarré."
                    if chosen else "Aucune expertise correspondante vérifiée ; préciser la mission."),
    }


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--mission", required=True)
    cli.add_argument("--manifest", default="agents/manifest-700-target.json")
    cli.add_argument("--role-id", default=None)
    cli.add_argument("--count", type=int, default=5)
    args = cli.parse_args()
    try:
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        result = route(manifest, args.mission, args.count, args.role_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["selected"] else 2)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
