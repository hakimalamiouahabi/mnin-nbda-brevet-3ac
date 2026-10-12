---
name: mnin-bridge-setup
description: Verify and guide MNIN Bridge setup for the MNIN NBDA Home, without allowing unauthorized or paid actions.
---

# MNIN Bridge setup

1. Read `README.md`, `mission_control.py` and `docs/ARCHITECTURE_ENTERPRISE_V02.md`.
2. Confirm the user owns or administers the repository and that branch names are feature/proposal branches.
3. Show the exact available operations and identify which are real vs merely documented.
4. Verify whether the MCP server is actually installed and authenticated. A local Python file is not a connected plugin.
5. If an asset is mentioned, require an actual binary in the approved private asset location, and calculate SHA-256 on the original bytes.
6. Never infer the contents of an unavailable attachment; never claim 700 agents are running because 700 profiles exist.
7. Start with the Home V1.0 approval. No external uploads of originals and no WordPress writes without direct approval.
8. Any new hosting, worker or GitHub Actions run must be checked for authorization and actual billing/quota policies first.
9. Keep all first-pass tests read-only and on isolated development copies; label outcome PASS/FAIL/NON TESTÉ/BLOQUÉ with evidence.
