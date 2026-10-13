#!/usr/bin/env python3
"""Sélectionne des profils EXACTEMENT présents au registre; aucun moteur d'IA externe."""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

STOPWORDS = frozenset("""
pour dans avec sans une des les sur the and de du et aux mon ma mes ton ta tes
notre nos votre vos tous tout toute chez qui quoi quand comment veux besoin plus
ce cet cette ces ne pas est sont un d l site outil projet equipe agents expert
""".split())

# Alias de missions, non pas de nouveaux profils : chaque cible est un INTITULÉ déjà catalogué.
RULES = {
    "incident": {
        "patterns": ("panne", "bug", "erreur", "incident", "ne fonctionne", "ne marche",
                     "plante", "bloque", "ne repond", "probleme technique", "dysfonctionnement"),
        "titles": ("Expert incident response", "QA automation", "Expert monitoring",
                   "Expert exploitation", "Ingénieur CI", "Expert rollback"),
    },
    "cloudflare": {
        "patterns": ("cloudflare", "workers", "worker", "d1", "kv", "r2"),
        "titles": ("Data architect", "Ingénieur base de données", "Data engineer",
                   "Expert intégrité", "Expert monitoring", "Expert AppSec"),
    },
    "wordpress": {
        "patterns": ("wordpress", "wp", "theme wordpress", "plugin wordpress", "gutenberg"),
        "titles": ("Architecte WordPress", "Expert plugin", "Expert thème",
                   "Expert sécurisation WordPress", "Expert Gutenberg"),
    },
    "database": {
        "patterns": ("base de donnees", "bases de donnees", "bdd", "sql", "database",
                     "doublon", "nettoyage", "donnees", "index"),
        "titles": ("Ingénieur base de données", "Data engineer", "Expert nettoyage",
                   "Expert intégrité", "Data architect", "Auditeur data"),
    },
    "performance": {
        "patterns": ("optimis", "lent", "lenteur", "rapid", "performance", "acceler"),
        "titles": ("Expert Core Web Vitals", "Expert LCP", "Expert optimisation mobile",
                   "Expert monitoring RUM", "Expert FinOps"),
    },
    "education": {
        "patterns": ("educat", "pedagog", "apprentiss", "eleve", "scolaire", "didact"),
        "titles": ("Ingénieur pédagogique", "Expert diagnostic", "Expert prérequis",
                   "Expert conception d'exercices", "Expert évaluation"),
    },
    "web": {
        "patterns": ("developp", "application", "logiciel", "web", "frontend"),
        "titles": ("Architecte WordPress", "Ingénieur frontend", "Développeur PHP",
                   "Expert API security", "QA automation"),
    },
}

# Les aides publiques et subventions sont hors du catalogue spécialisé MNIN NBDA.
# Ne jamais attribuer arbitrairement FinOps/finance-logicielle à l'analyse des aides publiques.
OUT_OF_SCOPE = ("subvention", "financement public", "aides publiques",
                "appel a projets", "credit impot recherche", "cir france")

def normalize(text):
    return unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode().lower()

def tokens(text):
    return {x for x in re.findall(r"[a-z0-9]+", normalize(text)) if len(x) >= 3 and x not in STOPWORDS}

def domains(text):
    normalized = normalize(text)
    return [name for name, spec in RULES.items() if any(pattern in normalized for pattern in spec["patterns"])]

def route(catalog, mission, count=5, role_id=None):
    profiles = catalog["profiles"]
    index = {p["id"]: p for p in profiles}
    if len(profiles) != 700 or len(index) != 700:
        raise ValueError("Le registre source ne contient pas 700 identifiants uniques")
    if not isinstance(mission, str) or not mission.strip():
        raise ValueError("Mission vide")
    if not 1 <= count <= 30:
        raise ValueError("count doit être compris entre 1 et 30")

    recognized = domains(mission)
    requested = tokens(mission)
    out_of_scope = any(p in normalize(mission) for p in OUT_OF_SCOPE)

    if role_id:
        if role_id not in index:
            raise ValueError("Identifiant inexistant dans le registre 700")
        chosen = [index[role_id]]
    elif out_of_scope and not recognized:
        chosen = []
    else:
        ranked = []
        for p in profiles:
            if p["level"] != "expert":
                continue
            title = p.get("title", "")
            title_tokens = tokens(title)
            group_tokens = tokens(p.get("competency_group", ""))
            base_score = 4 * len(requested & title_tokens) + len(requested & group_tokens)
            bonuses = []
            for name in recognized:
                titles = RULES[name]["titles"]
                if title in titles:
                    bonuses.append(10 - titles.index(title))
            score = base_score + sum(bonuses)
            if score:
                ranked.append((-score, p["id"], p))
        ranked.sort(key=lambda x: (x[0], x[1]))
        chosen = []
        seen_titles = set()
        for _, _, p in ranked:
            normalized_title = normalize(p["title"])
            if normalized_title in seen_titles:
                continue
            seen_titles.add(normalized_title)
            chosen.append(p)
            if len(chosen) >= count:
                break
    assignments = []
    for p in chosen:
        current = p
        chain = [{"id": p["id"], "title": p["title"]}]
        visited = {p["id"]}
        while current.get("parent_id") != "OWNER":
            parent_id = current.get("parent_id")
            if parent_id not in index or parent_id in visited:
                raise ValueError("Rattachement manquant ou hiérarchie cyclique")
            visited.add(parent_id)
            current = index[parent_id]
            chain.insert(0, {"id": current["id"], "title": current["title"]})
        assignments.append({"id": p["id"], "title": p["title"], "chain": chain,
                            "status": "ROLE_SELECTIONNE_NON_EXECUTE"})
    return {
        "status": "MATCHED" if assignments else "NO_DIRECT_MATCH",
        "mission": mission, "recognized_domains": recognized,
        "selected": len(assignments), "source_profiles": 700,
        "inference_started": False, "no_new_agents": True,
        "warning": ("Aucun expert direct dans les 700 profils catalogués; "
                    "ChatGPT peut répondre avec ses compétences générales sans inventer de rôle."
                    if not assignments else None),
        "assignments": assignments,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mission", required=True)
    parser.add_argument("--manifest", default="agents/manifest-700-target.json")
    parser.add_argument("--role-id", default=None)
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()
    try:
        catalog = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        print(json.dumps(route(catalog, args.mission, args.count, args.role_id),
                         ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False),
              file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
