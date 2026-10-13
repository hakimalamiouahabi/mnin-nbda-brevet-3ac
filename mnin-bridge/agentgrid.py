"""MNIN Bridge AgentGrid v0.8 — deterministic routing across 700 role definitions.

This is a *control-plane planner*, NOT a multi-LLM runtime. It does not spawn
models, call paid APIs, execute arbitrary code, or authorize WordPress writes.
A real execution requires an explicitly integrated, authenticated worker and
independent provider permissions. The owner and existing 43-agent catalog stay
unchanged.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

MANIFEST = Path(__file__).with_name("agentgrid") / "profiles-700.json"
EXPECTED = {"dsi": 5, "senior_manager": 30, "manager": 60,
            "team_leader": 60, "expert": 545}
LEVEL_ORDER = {"dsi": 0, "senior_manager": 1, "manager": 2,
               "team_leader": 3, "expert": 4}
MISSION_SPECS = {
    "home_8k_asset_qa": {
        "divisions": (1, 2, 5),
        "keywords": ("illustration", "vector", "svg", "8k", "logo", "image",
                     "responsive", "frontend", "qualite", "performance", "qa"),
        "goal": "Audit original art/assets, validate raster densities and real responsive screenshots",
    },
    "home_browser_qa": {
        "divisions": (1, 2, 5),
        "keywords": ("responsive", "frontend", "test", "qa", "accessibilite",
                     "performance", "experience", "typographie", "mobile"),
        "goal": "Real browser QA and evidence collection on approved staging copies",
    },
    "cloudflare_d1_readonly_audit": {
        "divisions": (4, 5, 2),
        "keywords": ("data", "sql", "gouvernance", "securite", "backup",
                     "sauvegarde", "restauration", "integrite", "finops", "audit"),
        "goal": "Read-only schema and maintenance assessment, with NO database cleanup",
    },
    "wordpress_readonly_audit": {
        "divisions": (2, 5, 1),
        "keywords": ("wordpress", "performance", "plugin", "backup", "restauration",
                     "securite", "php", "qa", "accessibilite", "compatibilite"),
        "goal": "Review staging WordPress and backups, without plugin changes or writes",
    },
    "github_maintenance_review": {
        "divisions": (2, 5, 4),
        "keywords": ("ci", "git", "devops", "test", "qa", "securite",
                     "data", "backup", "restauration", "finops"),
        "goal": "Inventory branch, artifact and security candidates without deletion or rewriting",
    },
    "curriculum_content_quality": {
        "divisions": (3, 1, 4),
        "keywords": ("referentiel", "programmes", "pedagog", "math",
                     "francais", "arabe", "science", "didactique", "evaluation"),
        "goal": "Review Moroccan 1AC/2AC/3AC content against checked official references",
    },
    "mcp_plugin_architecture": {
        "divisions": (2, 5, 4),
        "keywords": ("architecture", "api", "securite", "devops", "backend",
                     "data", "qa", "authentification", "integrations", "monitor"),
        "goal": "Plan owner-authenticated MCP read tools and external sandbox jobs",
    },
}
MAX_EXPERTS = 15
MAX_SIMULTANEOUS_JOBS = 3


def _normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    return "".join(c for c in value if not unicodedata.combining(c))


def _validate_manifest(data: dict) -> dict:
    profiles = data.get("profiles")
    if not isinstance(profiles, list) or len(profiles) != 700:
        raise ValueError("Expected exactly 700 individual role slots")
    identifiers = [p.get("id") for p in profiles]
    if len(set(identifiers)) != 700 or not all(
        isinstance(n, str) and re.fullmatch(r"[A-Z0-9_]+", n) for n in identifiers
    ):
        raise ValueError("Invalid or duplicate profile ids")
    by_id = {p["id"]: p for p in profiles}
    counts = Counter(p.get("level") for p in profiles)
    if dict(counts) != EXPECTED:
        raise ValueError(f"Unexpected hierarchy totals: {counts}")
    for p in profiles:
        if not isinstance(p.get("title"), str) or not 1 <= len(p["title"]) <= 180:
            raise ValueError("Profile missing human-readable job title")
        parent = p.get("parent_id")
        if p["level"] == "dsi":
            if parent != "OWNER":
                raise ValueError("DSI must report to owner")
        else:
            if parent not in by_id or LEVEL_ORDER[by_id[parent]["level"]] != LEVEL_ORDER[p["level"]] - 1:
                raise ValueError(f"Broken hierarchy at {p['id']}")
        if p["level"] == "expert" and not p.get("competency_group"):
            raise ValueError("Expert competency group missing")
    for p in profiles:
        cursor, chain, visited = p, [], set()
        while cursor["parent_id"] != "OWNER":
            if cursor["id"] in visited:
                raise ValueError("Cycle in role hierarchy")
            visited.add(cursor["id"])
            chain.append(cursor["id"])
            cursor = by_id[cursor["parent_id"]]
        if cursor["level"] != "dsi":
            raise ValueError("Profile must end at a DSI")
    return by_id


class AgentGrid:
    def __init__(self, manifest_path: Path | str = MANIFEST):
        path = Path(manifest_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        self.by_id = _validate_manifest(data)
        self.profiles = data["profiles"]

    def ancestors(self, profile_id: str) -> list[dict]:
        if profile_id not in self.by_id:
            raise ValueError("Unknown profile id")
        result, cursor = [], self.by_id[profile_id]
        while cursor["parent_id"] != "OWNER":
            cursor = self.by_id[cursor["parent_id"]]
            result.append(cursor)
        return list(reversed(result))

    def divisions(self) -> list[dict]:
        results = []
        for idx in range(1, 6):
            did = f"DSI_{idx:02d}"
            member_ids = [p["id"] for p in self.profiles
                          if p["id"] == did or self.ancestors(p["id"])[0]["id"] == did]
            counts = Counter(self.by_id[k]["level"] for k in member_ids)
            results.append({
                "dsi": did,
                "title": self.by_id[did]["title"],
                "profile_count": len(member_ids),
                "managers": counts["manager"],
                "senior_managers": counts["senior_manager"],
                "team_leaders": counts["team_leader"],
                "experts": counts["expert"],
            })
        return results

    def search(self, term: str, limit: int = 12) -> list[dict]:
        if not isinstance(term, str) or not 2 <= len(term) <= 100:
            raise ValueError("Search must be 2-100 characters")
        if not isinstance(limit, int) or not 1 <= limit <= 50:
            raise ValueError("Search limit must be 1-50")
        t = _normalize(term)
        found = [p for p in self.profiles
                 if t in _normalize(p["title"] + " " + p.get("competency_group", ""))]
        return [{"id": p["id"], "level": p["level"],
                 "title": p["title"], "parent_id": p["parent_id"]}
                for p in found[:limit]]

    def _dsi_id(self, p: dict) -> str:
        return p["id"] if p["level"] == "dsi" else self.ancestors(p["id"])[0]["id"]

    def route(self, kind: str, expert_limit: int = 9) -> dict:
        if kind not in MISSION_SPECS:
            raise ValueError("Mission must be from the fixed allowlist")
        if not isinstance(expert_limit, int) or not 1 <= expert_limit <= MAX_EXPERTS:
            raise ValueError(f"Expert limit must be 1-{MAX_EXPERTS}")
        spec = MISSION_SPECS[kind]
        allowed = [f"DSI_{i:02d}" for i in spec["divisions"]]
        keywords = [_normalize(x) for x in spec["keywords"]]
        candidate = []
        for p in self.profiles:
            if p["level"] != "expert":
                continue
            did = self._dsi_id(p)
            if did not in allowed:
                continue
            title = _normalize(p["title"])
            group = _normalize(p["competency_group"])
            score = 1 + sum((5 if kw in title else 0) +
                            (2 if kw in group else 0) for kw in keywords)
            candidate.append((score, allowed.index(did), p))
        # Balanced round-robin across relevant DSI domains; ties by ID.
        sorted_by_dsi = {}
        for did in allowed:
            local = [q for q in candidate if self._dsi_id(q[2]) == did]
            local.sort(key=lambda q: (-q[0], q[2]["id"]))
            sorted_by_dsi[did] = local
        chosen, unique = [], set()
        while len(chosen) < expert_limit:
            changed = False
            for did in allowed:
                while sorted_by_dsi[did] and sorted_by_dsi[did][0][2]["id"] in unique:
                    sorted_by_dsi[did].pop(0)
                if sorted_by_dsi[did] and len(chosen) < expert_limit:
                    p = sorted_by_dsi[did].pop(0)[2]
                    chosen.append(p)
                    unique.add(p["id"])
                    changed = True
            if not changed:
                break
        involved = {}
        for profile in chosen:
            involved[profile["id"]] = profile
            for manager in self.ancestors(profile["id"]):
                involved[manager["id"]] = manager
        ordered = sorted(involved.values(),
                         key=lambda p: (LEVEL_ORDER[p["level"]], self._dsi_id(p), p["id"]))
        return {
            "mission_kind": kind,
            "objective": spec["goal"],
            "selected_dsi": [d for d in allowed if d in {self._dsi_id(p) for p in chosen}],
            "total_profiles_in_registry": 700,
            "scheduled_expert_slots": len(chosen),
            "scheduled_hierarchy_slots": len(ordered),
            "expert_ids": [p["id"] for p in chosen],
            "roles": [{"id": p["id"], "level": p["level"], "title": p["title"],
                       "reports_to": p["parent_id"], "state": "PLANNED_NOT_RUNNING"}
                      for p in ordered],
            "actually_spawned_ai_agents": 0,
            "execution_status": "PLAN_ONLY",
            "calls_to_paid_ai_apis": 0,
            "write_operations_performed": 0,
            "notes": [
                "Profiles are job descriptions, not simultaneously running LLMs.",
                "Execution requires a separately connected and authorized worker.",
                "No WordPress write, Cloudflare purge or GitHub history rewrite.",
                "ChatGPT Pro custom MCP permissions cannot be bypassed.",
            ],
        }

    def portfolio(self, mission_kinds: list[str], expert_limit: int = 6,
                  max_concurrent_jobs: int = 2) -> dict:
        if not isinstance(mission_kinds, list) or not 1 <= len(mission_kinds) <= 5:
            raise ValueError("Portfolio must contain 1 to 5 mission kinds")
        if not isinstance(max_concurrent_jobs, int) or not 1 <= max_concurrent_jobs <= MAX_SIMULTANEOUS_JOBS:
            raise ValueError("Concurrency planning limit exceeded")
        if any(k not in MISSION_SPECS for k in mission_kinds):
            raise ValueError("Unrecognized mission in portfolio")
        if len(mission_kinds) != len(set(mission_kinds)):
            raise ValueError("Duplicate missions are not allowed")
        missions = [self.route(k, expert_limit=expert_limit) for k in mission_kinds]
        return {
            "portfolio_size": len(missions),
            "registry_count": 700,
            "max_concurrent_jobs_if_runner_enabled": max_concurrent_jobs,
            "actual_concurrent_jobs": 0,
            "actual_agents_running": 0,
            "batches": [
                [missions[k]["mission_kind"] for k in range(i, min(len(missions), i+max_concurrent_jobs))]
                for i in range(0, len(missions), max_concurrent_jobs)
            ],
            "missions": missions,
            "execution_status": "PLANNED_NO_RUNTIME",
            "max_incremental_eur": 0,
        }


def roster_status() -> dict:
    grid = AgentGrid()
    return {
        "status": "ROSTER_LINKED_TO_PLUGIN_NOT_RUNNING",
        "counts": dict(Counter(p["level"] for p in grid.profiles)),
        "total_profiles": len(grid.profiles),
        "divisions": grid.divisions(),
        "mission_kinds": sorted(MISSION_SPECS),
        "max_experts_per_plan": MAX_EXPERTS,
        "max_concurrent_jobs_planned": MAX_SIMULTANEOUS_JOBS,
        "authenticated_mcp_runtime": "NOT CONNECTED",
        "agents_running": 0,
        "paid_ai_api_enabled": False,
    }
