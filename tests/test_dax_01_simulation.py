import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dax_01_simulation import DAX01TopologyEvaluator

class TestDAX01TopologyEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = DAX01TopologyEvaluator()
        self.draft_code = 'client.post("/api/v2/auth", data={"t": "abc", "c": "123"})'

    def test_successful_transduction(self):
        res = self.evaluator.empathy_code_transduction(
            "We reproduced the auth failure.",
            "401",
            "/api/v2/auth",
            self.draft_code,
            ["token", "client_id"],
            10
        )
        self.assertIn("Expected Output: 200 OK", res)
        self.assertIn("Fix:", res)

    def test_anionic_veto(self):
        with self.assertRaises(ValueError) as context:
            self.evaluator.empathy_code_transduction(
                "This is a revolutionary fix.",
                "401",
                "/api/v2/auth",
                self.draft_code,
                ["token", "client_id"],
                10
            )
        self.assertIn("Anionic Veto triggered", str(context.exception))

    def test_dccd_schema_guard_failure(self):
        bad_code = 'client.post("/api/v2/auth", data={"token": "abc"})'
        with self.assertRaises(ValueError) as context:
            self.evaluator.empathy_code_transduction(
                "We see the issue.",
                "401",
                "/api/v2/auth",
                bad_code,
                ["token"],
                10
            )
        self.assertIn("DCCDSchemaGuard validation failed", str(context.exception))

if __name__ == '__main__':
    unittest.main()
