"""MNIN Bridge mission control v0.2.

Stores bounded, reviewable mission proposals. This module DOES NOT execute code,
spawn agents, call remote APIs or grant access to files/WordPress. All missions
start as PLANNED. Execution requires a separately implemented, authenticated
approver and an isolated worker — neither is included in this version.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

BRANCH = re.compile(r"^(feature|proposal)/[A-Za-z0-9][A-Za-z0-9._/-]{0,110}$")
SAFE_REL = re.compile(r"^(site|home|preview)/[A-Za-z0-9._/-]+\.html$")
SAFE_IMAGE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,159}\.(?:png|jpg|jpeg|webp|svg)$", re.I)
KINDS = {
    "asset_integrity": {
        "required": {"filename"},
        "roles": ["DESIGN_CONTENT", "QA_AUTOMATION"],
        "result": "Original-byte SHA-256, file size, intrinsic image dimensions"},
    "home_browser_qa": {
        "required": {"branch", "home_path"},
        "roles": ["FRONTEND_UI", "RESPONSIVE_MOBILE", "QA_AUTOMATION"],
        "result": "Viewport/full-page captures plus reproducible browser QA"},
    "home_visual_review": {
        "required": {"branch", "home_path", "filename"},
        "roles": ["DESIGN_CONTENT", "UX_ACCESSIBILITY", "QA_AUTOMATION"],
        "result": "Review visual deviations relative to a separately verified reference"},
    "home_asset_audit": {
        "required": {"branch", "home_path"},
        "roles": ["DESIGN_CONTENT", "PERFORMANCE_WP"],
        "result": "Raster resolution, SVG availability, broken-image warnings"},
    "home_accessibility_review": {
        "required": {"branch", "home_path"},
        "roles": ["UX_ACCESSIBILITY", "QA_LOCALIZATION"],
        "result": "Accessibility test evidence, not a WCAG certification"},
}
ALLOWED_KEYS = {"filename", "branch", "home_path"}
IDEMPOTENCY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,95}$")
JOB_ID = re.compile(r"^[a-f0-9]{32}$")
STATUSES = {"PLANNED", "BLOCKED", "AWAITING_APPROVAL", "APPROVED", "RUNNING", "PASS", "FAIL"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def validate_request(kind: str, inputs: dict) -> dict:
    if kind not in KINDS:
        raise ValueError("Task kind not in approved capability catalog")
    if not isinstance(inputs, dict) or set(inputs) != KINDS[kind]["required"]:
        raise ValueError("Mission inputs must contain exactly the required fields")
    for key, val in inputs.items():
        if key not in ALLOWED_KEYS or not isinstance(val, str) or len(val) > 160:
            raise ValueError("Unsupported or oversized mission input")
        if key == "filename" and not SAFE_IMAGE.fullmatch(val):
            raise ValueError("filename must be a simple supported image name")
        if key == "branch" and (not BRANCH.fullmatch(val) or ".." in val or "//" in val):
            raise ValueError("Only safe feature/ or proposal/ branches are allowed")
        if key == "home_path" and (not SAFE_REL.fullmatch(val) or ".." in val or "//" in val):
            raise ValueError("Only an approved relative HTML path is allowed")
    return dict(sorted(inputs.items()))


def capability_catalog() -> dict:
    return {
        "version": "0.2.0",
        "capabilities": [{"kind": k, "required_fields": sorted(v["required"]),
                          "roles": v["roles"], "expected_result": v["result"]}
                         for k, v in KINDS.items()],
        "execution": "NO RUNNER ACTIVATED",
        "agent_orchestration": "ROLES PLANNED, NOT SPAWNED",
        "wordpress_writes": False,
        "model_api_charges": False,
    }


class MissionStore:
    """SQLite-based mission planning and event audit. Not an execution queue."""

    def __init__(self, state_dir: str | Path | None = None):
        raw = state_dir or os.environ.get("MNIN_STATE_DIR", "")
        if not raw:
            raise RuntimeError("MNIN_STATE_DIR must point to a private persistent folder")
        self.root = Path(raw).expanduser().resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError("MNIN_STATE_DIR must be an existing directory")
        self.path = self.root / "missions.sqlite3"
        with self._db() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS missions (
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                inputs_json TEXT NOT NULL,
                state TEXT NOT NULL CHECK (state IN (
                    'PLANNED','BLOCKED','AWAITING_APPROVAL',
                    'APPROVED','RUNNING','PASS','FAIL')),
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                idempotency_key TEXT UNIQUE
            )""")
            db.execute("""CREATE TABLE IF NOT EXISTS audit (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                mission_id TEXT NOT NULL,
                action TEXT NOT NULL,
                at TEXT NOT NULL,
                detail TEXT NOT NULL,
                FOREIGN KEY (mission_id) REFERENCES missions(id)
            )""")

    def _db(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("PRAGMA busy_timeout=10000")
        return db

    @staticmethod
    def _record(row) -> dict:
        return {"mission_id": row["id"], "kind": row["kind"],
                "inputs": json.loads(row["inputs_json"]), "status": row["state"],
                "created_at": row["created_at"], "updated_at": row["updated_at"]}

    def propose(self, kind: str, inputs: dict, idempotency_key: str = "") -> dict:
        clean = validate_request(kind, inputs)
        if idempotency_key and not IDEMPOTENCY.fullmatch(idempotency_key):
            raise ValueError("Invalid idempotency key")
        now = _utc_now()
        identifier = uuid.uuid4().hex
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            if idempotency_key:
                previous = db.execute(
                    "SELECT * FROM missions WHERE idempotency_key=?",
                    (idempotency_key,)).fetchone()
                if previous:
                    if previous["kind"] != kind or json.loads(previous["inputs_json"]) != clean:
                        raise ValueError("Idempotency key already used for a different mission")
                    return self._record(previous)
            db.execute(
                """INSERT INTO missions
                (id,kind,inputs_json,state,created_at,updated_at,idempotency_key)
                VALUES (?,?,?,?,?,?,?)""",
                (identifier, kind, json.dumps(clean, sort_keys=True),
                 "PLANNED", now, now, idempotency_key or None))
            db.execute("INSERT INTO audit(mission_id,action,at,detail) VALUES(?,?,?,?)",
                       (identifier, "proposed", now, "No execution started"))
        return self.read(identifier)

    def read(self, mission_id: str) -> dict:
        if not isinstance(mission_id, str) or not JOB_ID.fullmatch(mission_id):
            raise ValueError("Invalid mission id")
        with self._db() as db:
            row = db.execute("SELECT * FROM missions WHERE id=?", (mission_id,)).fetchone()
        if row is None:
            raise KeyError("Mission not found")
        return self._record(row)

    def list(self, limit: int = 20) -> list[dict]:
        if not isinstance(limit, int) or not 1 <= limit <= 100:
            raise ValueError("Limit must be between 1 and 100")
        with self._db() as db:
            rows = db.execute(
                "SELECT * FROM missions ORDER BY created_at DESC, id DESC LIMIT ?",
                (limit,)).fetchall()
        return [self._record(row) for row in rows]

    def audit(self, mission_id: str) -> list[dict]:
        self.read(mission_id)
        with self._db() as db:
            rows = db.execute(
                "SELECT event_id,action,at,detail FROM audit WHERE mission_id=? ORDER BY event_id",
                (mission_id,)).fetchall()
        return [dict(row) for row in rows]

    def preview(self, mission_id: str) -> dict:
        mission = self.read(mission_id)
        spec = KINDS[mission["kind"]]
        return {
            "mission": mission,
            "roles_requested": spec["roles"],
            "roles_spawned": 0,
            "expected_result": spec["result"],
            "steps": [
                "Validate available original files and safe checkout",
                "Require separate verified owner approval before any execution",
                "Run in a sandbox without WordPress write credentials",
                "Preserve logs, report and output artifact references",
                "Require owner sign-off before any WordPress change",
            ],
            "execution_possible_now": False,
            "blockers": [
                "Authenticated MCP connection not deployed",
                "Independent approver not implemented",
                "Isolated execution worker not activated",
            ],
        }
