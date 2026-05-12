from dax_01_simulation import DAX01TopologyEvaluator
import unittest
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestDAX01TopologyEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = DAX01TopologyEvaluator()
        self.draft_code = 'client.post("/api/v2/auth", data={"t": "abc", "c": "123"})'  # noqa: E501

    def test_successful_transduction(self):
        """Happy Path: Standard successful transduction"""
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
        self.assertIn("Scar ID: VSA_HV_", res)

    def test_anionic_veto(self):
        """Error Case: Anionic Veto triggered"""
        with pytest.raises(ValueError, match="Anionic Veto triggered"):
            self.evaluator.empathy_code_transduction(
                "This is a revolutionary fix.",
                "401",
                "/api/v2/auth",
                self.draft_code,
                ["token", "client_id"],
                10
            )

    def test_dccd_schema_guard_failure(self):
        """Error Case: DCCDSchemaGuard validation failure"""
        bad_code = 'client.post("/api/v2/auth", data={"token": "abc"})'
        with pytest.raises(ValueError, match="DCCDSchemaGuard validation failed"):  # noqa: E501
            self.evaluator.empathy_code_transduction(
                "We see the issue.",
                "401",
                "/api/v2/auth",
                bad_code,
                ["token"],
                10
            )

    def test_unsafe_operations_in_production(self):
        """Error Case: Unsafe operations in production environment"""
        unsafe_code = 'import os; os.system("rm -rf /") # unsafe'
        with pytest.raises(ValueError, match="Transduction rejected: unsafe operations in production."):  # noqa: E501
            self.evaluator.empathy_code_transduction(
                "Fix for cleanup.",
                "401",
                "/api/v2/auth",
                unsafe_code,
                ["token", "client_id"],
                10,
                target_environment="production"
            )

    def test_unsafe_operations_in_development(self):
        """Happy Path: Unsafe operations are allowed in non-production environment"""  # noqa: E501
        unsafe_code = 'import os; os.system("rm -rf /") # unsafe'
        res = self.evaluator.empathy_code_transduction(
            "Fix for cleanup.",
            "401",
            "/api/v2/auth",
            unsafe_code,
            ["token", "client_id"],
            10,
            target_environment="development"
        )
        self.assertIn("Fix: import os; os.system(\"rm -rf /\") # unsafe", res)

    def test_ssi_calculation_exists(self):
        """Edge Case: SSI calculation for empty text"""
        # SSI for empty text should be 1.0 per implementation
        ssi = self.evaluator.calculate_ssi("", 10)
        self.assertEqual(ssi, 1.0)

    def test_enforce_dccd_schema_guard_missing_endpoint(self):
        """Edge Case: Endpoint not in AST mock returns False immediately"""
        is_valid = self.evaluator.enforce_dccd_schema_guard(
            self.draft_code, "/nonexistent/endpoint", ["token", "client_id"]
        )
        self.assertFalse(is_valid)

    def test_empathy_code_transduction_low_ssi(self):
        """Edge Case: Low SSI condition hit"""
        res = self.evaluator.empathy_code_transduction(
            "auth failed",  # 2 words
            "401",
            "/api/v2/auth",
            self.draft_code,
            ["token", "client_id"],
            1  # 1 / 2 = 0.5 SSI
        )
        self.assertIn("Expected Output: 200 OK", res)


if __name__ == '__main__':
    unittest.main()
