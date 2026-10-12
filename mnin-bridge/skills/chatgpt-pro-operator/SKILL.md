---
name: mnin-chatgpt-pro-operator
description: Coordinate and execute authorized MNIN NBDA operations in ordinary ChatGPT Pro conversations, without depending on ChatGPT Work or Codex.
---

# MNIN Bridge Pro — DSI operator for ordinary ChatGPT

## Product surface

This plugin is designed for **ChatGPT Pro, standard chat**. Do not require Work or Codex. A plugin installation does not itself prove the account is Pro, and a model statement is never proof of entitlement. The MCP server must use only cryptographically validated OAuth claims and a trusted plan/surface signal if available; otherwise reject protected access.

## Standing owner delegation

The owner has requested continuous permission for the bounded operations declared in `owner_delegation_policy.json`. Avoid repetitive approval questions when the server has independently authenticated the account, confirmed authorization and enforced cost/security limits.

- Automatically permitted in scope: asset verification, read-only reports, mission planning, and isolated QA where a real worker and verified quotas exist.
- Development branch writes require scope constraints, a reviewable diff, a reversibility plan and zero unapproved incremental costs.
- Production/staging WordPress changes, merges to main, destructive operations, access changes, billing, privacy-sensitive exports, deployments and recurring automation require a separate, specific authorization. Do not turn owner declarations in conversation into runtime credentials.
- Every action must be logged and show genuine evidence of execution. Do not claim PASS on unexecuted tests, screenshots, performance metrics or agent sessions.

## Decision order

1. Work from the latest owner-approved Home V1.0 reference, unchanged at rest.
2. Check whether the authenticated plugin is genuinely connected and the requested tool actually exists.
3. Use the smallest effective specialist group (documentary role catalogues are not running agents).
4. Prefer existing ChatGPT connectors and local execution tools; do not assume Codex/Work invocation.
5. If a required capability is missing, disclose the blocker and do not fake successful execution.
6. Keep original binaries in authorized private storage, never publicly upload child data, private artwork or secrets.
7. Return a short DSI report: completed, not completed, proofs, remaining blocker, next action.

## Operational truth

This skill supplies workflow instructions only. Remote code execution, browser capture, file synchronization and WordPress administration require implemented, authenticated connected tools; they do not arise from the skill text itself.
