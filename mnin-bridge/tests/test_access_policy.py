"""Tests: policy honors standing consent without trusting model-supplied approval."""
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from access_policy import (
    VerifiedPrincipal, public_policy_summary, evaluate_delegation,
    ensure_delegated, _load_policy,
)

ENV = {
    "MNIN_DELEGATION_ACTIVE": "1",
    "MNIN_OWNER_SUB": "verified-owner-subject",
    "MNIN_OAUTH_ISSUER": "https://issuer.example",
    "MNIN_OAUTH_AUDIENCE": "https://mnin.example/mcp",
    "MNIN_CHATGPT_STANDARD_CLIENT_ID": "oauth-client-chatgpt-standard",
}

def principal(**overrides):
    props = {
        "subject": "verified-owner-subject",
        "issuer": "https://issuer.example",
        "audience": "https://mnin.example/mcp",
        "client_id": "oauth-client-chatgpt-standard",
        "token_scopes": frozenset({"mnin:read","mnin:plan","mnin:qa","mnin:dev"}),
        "auth_verified": True,
        "product_surface": "chatgpt_standard",
        "surface_verified": True,
        "subscription": "pro",
        "subscription_verified": True,
    }
    props.update(overrides)
    return VerifiedPrincipal(**props)

class OwnerDelegationTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, ENV)
        env.start()
        self.addCleanup(env.stop)

    def test_schema_readable_and_non_bypassable_high_risk(self):
        p = _load_policy()
        self.assertEqual(p["identity_gate"]["target_subscription"], "Pro")
        self.assertTrue(p["standing_delegation"]["enabled"])
        self.assertNotIn("wordpress.production_write",
                         p["standing_delegation"]["allow_without_reprompt"])
        self.assertIn("wordpress.production_write",
                      p["standing_delegation"]["requires_per_action_approval"])

    def test_permanent_delegation_for_bounded_actions(self):
        for action in ("asset.verify","asset.list","mission.propose","mission.read","qa.preview"):
            with self.subTest(action=action):
                self.assertEqual(evaluate_delegation(action, principal())["status"], "DELEGATED")

    def test_risky_but_reversible_actions_conditional(self):
        for action in ("qa.run_isolated", "dev.branch_write", "report.create"):
            with self.subTest(action=action):
                result = evaluate_delegation(action, principal())
                self.assertEqual(result["status"], "DELEGATED_CONDITIONAL")
                self.assertIn("conditions", result)

    def test_destructive_requires_independent_approval(self):
        for action in ("wordpress.production_write","wordpress.staging_write",
                       "github.merge_to_main","hosting.deploy_public","billing.charge",
                       "domain.dns_change","mass_delete"):
            with self.subTest(action=action):
                self.assertEqual(evaluate_delegation(action, principal())["status"],
                                 "AWAITING_SPECIFIC_APPROVAL")

    def test_absolutely_blocked(self):
        for action in ("secrets.export","child_data.export","unrestricted_shell",
                       "unbounded_agent_execution"):
            with self.subTest(action=action):
                self.assertEqual(evaluate_delegation(action, principal())["status"],"DENY")

    def test_no_authenticated_context(self):
        self.assertEqual(evaluate_delegation("asset.list", None)["status"],"DENY")

    def test_oauth_not_verified(self):
        self.assertEqual(evaluate_delegation("asset.list", principal(auth_verified=False))["status"],"DENY")

    def test_mismatched_owner(self):
        self.assertEqual(evaluate_delegation("asset.list",principal(subject="attacker"))["status"],"DENY")

    def test_mismatched_issuer(self):
        self.assertEqual(evaluate_delegation("asset.list",principal(issuer="https://other.example"))["status"],"DENY")

    def test_mismatched_resource(self):
        self.assertEqual(evaluate_delegation("asset.list",principal(audience="https://evil.example"))["status"],"DENY")

    def test_block_codex(self):
        self.assertEqual(evaluate_delegation("asset.list",principal(product_surface="codex"))["status"],"DENY")

    def test_block_work(self):
        self.assertEqual(evaluate_delegation("asset.list",principal(product_surface="work"))["status"],"DENY")

    def test_unverified_surface(self):
        self.assertEqual(evaluate_delegation("asset.list",principal(surface_verified=False))["status"],"DENY")

    def test_unverified_pro(self):
        self.assertEqual(evaluate_delegation("asset.list",principal(subscription_verified=False))["status"],"DENY")

    def test_not_pro(self):
        self.assertEqual(evaluate_delegation("asset.list",principal(subscription="plus"))["status"],"DENY")

    def test_not_valid_oauth_client(self):
        self.assertEqual(evaluate_delegation("asset.list",principal(client_id="codex-client"))["status"],"DENY")

    def test_missing_oauth_scope(self):
        self.assertEqual(evaluate_delegation("dev.branch_write",principal(token_scopes=frozenset({"mnin:read"})))["status"],"DENY")

    def test_requires_external_activation(self):
        with patch.dict(os.environ,{"MNIN_DELEGATION_ACTIVE":"0"}):
            self.assertEqual(evaluate_delegation("asset.list",principal())["status"],"DENY")

    def test_unknown_operation_denied(self):
        self.assertEqual(evaluate_delegation("arbitrary_tool.invoke",principal())["status"],"DENY")

    def test_strict_check_raises(self):
        with self.assertRaises(PermissionError):
            ensure_delegated("billing.charge",principal())

    def test_public_info_omits_owner(self):
        s=public_policy_summary()
        self.assertNotIn("subject",s)
        self.assertNotIn("verified-owner-subject",json.dumps(s))

if __name__ == "__main__":
    unittest.main()
