import unittest
import time
import json


class KIRA7TopologyEvaluator:
    def __init__(self):
        self.petzold_state = "THINK"
        self.token_cache = {}

    def enforce_petzold_transition(self, new_state: str):
        """
        Rule 5: Personality Containment (Petzold Loop Enforcement).
        Transitions between THINK, WRITE, CODE, IMMUNE_REVIEW.
        """
        valid_transitions = {
            "THINK": ["WRITE"],
            "WRITE": ["CODE"],
            "CODE": ["IMMUNE_REVIEW"],
            "IMMUNE_REVIEW": ["THINK", "WRITE"]
        }

        if new_state not in valid_transitions.get(self.petzold_state, []):
            raise ValueError(
                f"Invalid Petzold transition from "
                f"{self.petzold_state} to {new_state}")

        self.petzold_state = new_state
        return self.petzold_state

    def check_dccd_schema_guard(self, payload_str: str) -> bool:
        """
        Rule 1: The Anionic Veto on JSON (DCCDSchemaGuard).
        NEVER output Feishu Message Card JSON without passing through
        the schema.
        Simulating a check for Feishu Card JSON v2.0 'msg_type: interactive'.
        """
        try:
            payload = json.loads(payload_str)
            if payload.get("msg_type") != "interactive":
                return False
            if "card" not in payload:
                return False
            # Simulate validating field tags and depth
            if not isinstance(payload["card"], dict):
                return False
            return True
        except json.JSONDecodeError:
            return False

    def get_tenant_access_token(self, token_id: str) -> str:
        """
        Rule 2: Token Primacy (SagaRecovery).
        Never call POST /auth/v3/... without checking cache first.
        """
        current_time = time.time()
        if token_id in self.token_cache:
            cache_entry = self.token_cache[token_id]
            if current_time < cache_entry['expires_at']:
                return cache_entry['token']

        # Simulate fetching a new token
        new_token = f"t-{token_id}-new"
        # 6900 TTL for safety buffer
        self.token_cache[token_id] = {
            'token': new_token,
            'expires_at': current_time + 6900
        }
        return new_token

    def verify_zero_trust_ingress(
            self,
            has_challenge: bool,
            has_decrypt: bool,
            has_valid_signature: bool,
            timestamp_freshness_seconds: int) -> bool:
        """
        Rule 3: Webhook Sovereignty (Zero-Trust Ingress).
        """
        if has_challenge:
            return True  # Immediately return challenge, skip other checks

        if not has_decrypt:
            return False

        if not has_valid_signature:
            return False

        if timestamp_freshness_seconds > 300:
            return False

        return True


class TestKIRA7Rules(unittest.TestCase):
    def test_dccd_schema_guard_pass(self):
        evaluator = KIRA7TopologyEvaluator()
        valid_json = '{"msg_type": "interactive", "card": {"elements": []}}'
        self.assertTrue(evaluator.check_dccd_schema_guard(valid_json))

    def test_dccd_schema_guard_fail_wrong_type(self):
        evaluator = KIRA7TopologyEvaluator()
        invalid_json = '{"msg_type": "text", "content": "hello"}'
        self.assertFalse(evaluator.check_dccd_schema_guard(invalid_json))

    def test_dccd_schema_guard_fail_no_card(self):
        evaluator = KIRA7TopologyEvaluator()
        invalid_json = '{"msg_type": "interactive", "elements": []}'
        self.assertFalse(evaluator.check_dccd_schema_guard(invalid_json))

    def test_petzold_loop_transitions(self):
        evaluator = KIRA7TopologyEvaluator()
        self.assertEqual(evaluator.petzold_state, "THINK")
        evaluator.enforce_petzold_transition("WRITE")
        self.assertEqual(evaluator.petzold_state, "WRITE")
        evaluator.enforce_petzold_transition("CODE")
        self.assertEqual(evaluator.petzold_state, "CODE")
        evaluator.enforce_petzold_transition("IMMUNE_REVIEW")
        self.assertEqual(evaluator.petzold_state, "IMMUNE_REVIEW")

        with self.assertRaises(ValueError):
            evaluator.enforce_petzold_transition("CODE")

    def test_token_primacy_caching(self):
        evaluator = KIRA7TopologyEvaluator()
        token1 = evaluator.get_tenant_access_token("tenant_a")
        self.assertEqual(token1, "t-tenant_a-new")

        # Next call should return same token
        token2 = evaluator.get_tenant_access_token("tenant_a")
        self.assertEqual(token1, token2)

        # Expire cache manually
        evaluator.token_cache["tenant_a"]["expires_at"] = time.time() - 100
        token3 = evaluator.get_tenant_access_token("tenant_a")
        # Should still fetch new token with updated logic
        self.assertTrue(token3.startswith("t-tenant_a"))

    def test_zero_trust_ingress(self):
        evaluator = KIRA7TopologyEvaluator()

        # Challenge overrides
        self.assertTrue(evaluator.verify_zero_trust_ingress(
            True, False, False, 1000))

        # Valid webhook
        self.assertTrue(evaluator.verify_zero_trust_ingress(
            False, True, True, 10))

        # Missing Decrypt
        self.assertFalse(evaluator.verify_zero_trust_ingress(
            False, False, True, 10))

        # Invalid Signature
        self.assertFalse(evaluator.verify_zero_trust_ingress(
            False, True, False, 10))

        # Stale Timestamp
        self.assertFalse(evaluator.verify_zero_trust_ingress(
            False, True, True, 301))


if __name__ == '__main__':
    unittest.main()
