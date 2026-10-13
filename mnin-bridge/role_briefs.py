"""MNIN Bridge role contracts for EXACTLY the 700 EXISTING profiles.

This module formats role instructions/quality obligations for use by a human or
the single ChatGPT model during a permitted conversation. Creating a brief does
not create or run an AI agent. No additional profiles, API or infrastructure.
"""
from __future__ import annotations

import json
from pathlib import Path

from agentgrid import AgentGrid, MISSION_SPECS

QUALITY_BY_LEVEL = {
    "dsi": "Valider le perimetre, les dependances, les risques, le cout et l'accord du proprietaire.",
    "senior_manager": "Definir les criteres d'acceptation et etablir les arbitrages documentes.",
    "manager": "Decouper le travail en operations testables et planifier une validation croisee.",
    "team_leader": "Verifier les artefacts, les tests et les ecarts avant livraison.",
    "expert": "Produire des observations verifiables uniquement dans sa competence documentee.",
}
DOMAIN_CHECKS = {
    "DSI_01": [
        "Comparer les maquettes responsive a la Home V1.0 approuvee.",
        "Verifier la resolution native des logos, SVG, illustrations et assets raster.",
        "Exiger preuves de captures, tests d'accessibilite et validation humaine.",
    ],
    "DSI_02": [
        "Verifier la compatibilite WordPress/PHP/JS et l'architecture des modules.",
        "Mettre les changements de code sur une branche isolee avec tests.",
        "Verifier performance, security review et plan de retour arriere.",
    ],
    "DSI_03": [
        "Verifer les notions et exercices contre les programmes marocains 1AC/2AC/3AC.",
        "Distinguer les hypotheses pedagogiques des contenus controles.",
        "Exiger une revue humaine des corriges et des sources de reference.",
    ],
    "DSI_04": [
        "Etablir une tracabilite des donnees et une separation stricte des comptes.",
        "Ne pas lire ni exposer de donnees personnelles d'eleves lors des tests.",
        "Verifier la validite des donnees et les indicateurs avant conclusion.",
    ],
    "DSI_05": [
        "Verifier permissions, sauvegarde, restauration et politique de cout nul.",
        "Conserver l'historique d'audit et ne pas effacer les journaux.",
        "Documenter les risques, les alertes et le statut PASS/FAIL/BLOQUE.",
    ],
}

SAFETY = [
    "Ne jamais declarer avoir execute un outil, un test, un modele ou un agent sans preuve.",
    "Aucune nouvelle API IA payante, depense ou abonnement.",
    "Aucun acces WordPress en ecriture sans confirmation separee et sauvegarde.",
    "Aucune purge D1, suppression Git ou export de donnees personnelles.",
    "Toujours signaler PASS, FAIL, NON TESTE ou BLOQUE avec preuve.",
]


def role_brief(profile_id: str, mission_kind: str = "", _grid: AgentGrid | None = None) -> dict:
    grid = _grid if _grid is not None else AgentGrid()
    if not isinstance(profile_id, str) or profile_id not in grid.by_id:
        raise ValueError("Only original profile identifiers are supported")
    if mission_kind and mission_kind not in MISSION_SPECS:
        raise ValueError("Unknown mission type")
    p = grid.by_id[profile_id]
    chain = grid.ancestors(profile_id)
    dsi = p["id"] if p["level"] == "dsi" else chain[0]["id"]
    return {
        "role_id": p["id"],
        "role_title": p["title"],
        "level": p["level"],
        "competency_group": p.get("competency_group", ""),
        "management_chain": [a["id"] for a in chain],
        "dsi_id": dsi,
        "mission_kind": mission_kind or "UNASSIGNED",
        "mission_goal": MISSION_SPECS[mission_kind]["goal"] if mission_kind else None,
        "professional_quality_gate": QUALITY_BY_LEVEL[p["level"]],
        "domain_quality_checks": DOMAIN_CHECKS[dsi],
        "instructions": [
            "Utiliser uniquement les informations disponibles et les outils reels autorises.",
            "Travailler sous le role exact defini dans le catalogue MNIN NBDA existant.",
            "Separarer recommandations, preuves d'execution et hypotheses.",
            "Produire un livrable verifiable avec les limites, ecarts et prochaines actions.",
            *SAFETY,
        ],
        "profile_source": "agentgrid/profiles-700.json",
        "is_new_role": False,
        "independent_ai_agent_running": False,
        "execution": "ROLE_BRIEF_ONLY",
    }


def full_contract_inventory() -> dict:
    grid = AgentGrid()
    contracts = [role_brief(p["id"], _grid=grid) for p in grid.profiles]
    if len(contracts) != 700 or len({c["role_id"] for c in contracts}) != 700:
        raise RuntimeError("Generated role contracts must match the exact original roster")
    return {
        "status": "GENERATED_ROLE_CONTRACTS_NOT_LLM_SESSIONS",
        "total_existing_roles": len(contracts),
        "additional_roles_created": 0,
        "individual_ai_agents_running": 0,
        "contracts": contracts,
    }


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="mnin-bridge-qa-results/agentgrid-700-role-contracts.json")
    args = parser.parse_args()
    output = Path(args.output)
    if output.is_absolute() or ".." in output.parts or output.suffix != ".json":
        raise ValueError("Output must be a safe relative JSON path")
    payload = full_contract_inventory()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
    print(f"AGENTGRID_ROLE_CONTRACTS_PASS: {len(payload['contracts'])} existing profiles; 0 new roles; 0 LLM sessions")


if __name__=="__main__":
    main()
