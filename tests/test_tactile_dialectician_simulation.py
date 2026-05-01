import unittest
import torch
from tactile_dialectician_simulation import TactileDialecticianV6Evaluator


class TestTactileDialecticianV6Evaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = TactileDialecticianV6Evaluator()

    def test_calculate_topological_derivative_no_dissonance(self):
        # Exact same position
        force = self.evaluator.calculate_topological_derivative(5.0, 5.0)
        self.assertAlmostEqual(force, 0.0)

        # Within epsilon
        force = self.evaluator.calculate_topological_derivative(
            5.0, 5.0 + (self.evaluator.epsilon / 2))
        self.assertAlmostEqual(force, 0.0)

    def test_calculate_topological_derivative_with_dissonance(self):
        pos_a = 10.0
        pos_b = 2.0
        expected_force = abs(10.0 - 2.0) * 1.618

        force = self.evaluator.calculate_topological_derivative(pos_a, pos_b)

        torch.testing.assert_close(
            torch.tensor(force),
            torch.tensor(expected_force),
            rtol=1e-3,
            atol=1e-3
        )

    def test_evaluate_epsilon_tolerance_tech_debt_transition_fit(self):
        # Exactly 1.0
        status = self.evaluator.evaluate_epsilon_tolerance_tech_debt(1.0)
        self.assertEqual(status, "Transition Fit")

        # Within positive epsilon
        status = self.evaluator.evaluate_epsilon_tolerance_tech_debt(
            1.0 + (self.evaluator.epsilon / 2))
        self.assertEqual(status, "Transition Fit")

        # Within negative epsilon (magnitude)
        status = self.evaluator.evaluate_epsilon_tolerance_tech_debt(
            -1.0 + (self.evaluator.epsilon / 2))
        self.assertEqual(status, "Transition Fit")

    def test_evaluate_epsilon_tolerance_tech_debt_structural_failure(self):
        status = self.evaluator.evaluate_epsilon_tolerance_tech_debt(1.5)
        self.assertEqual(status, "Structural Failure")

        status = self.evaluator.evaluate_epsilon_tolerance_tech_debt(0.0)
        self.assertEqual(status, "Structural Failure")

        status = self.evaluator.evaluate_epsilon_tolerance_tech_debt(-1.5)
        self.assertEqual(status, "Structural Failure")

    def test_anti_sycophancy_evaluation_success(self):
        rate = self.evaluator.anti_sycophancy_evaluation(96, 100)
        self.assertAlmostEqual(rate, 96.0)

        rate = self.evaluator.anti_sycophancy_evaluation(100, 100)
        self.assertAlmostEqual(rate, 100.0)

    def test_anti_sycophancy_evaluation_zero_prompts(self):
        rate = self.evaluator.anti_sycophancy_evaluation(0, 0)
        self.assertAlmostEqual(rate, 0.0)

    def test_anti_sycophancy_evaluation_failure(self):
        with self.assertRaises(ValueError) as context:
            self.evaluator.anti_sycophancy_evaluation(90, 100)

        self.assertTrue("Anti-Sycophancy failure" in str(context.exception))

        with self.assertRaises(ValueError):
            self.evaluator.anti_sycophancy_evaluation(95, 100)

    def test_metrological_conformance_check_pass(self):
        valid_fcf = """
        # DATUMS:
        #   A: ROLE(Strategic Integration Project Manager)
        # FEATURES:
        #       - CONTROL(FORM) | TYPE(Text, Paragraph)
        #       - CONTROL(ORIENTATION) | TYPE(TONAL_CONSISTENCY) | DATUM(A)
        """
        self.assertTrue(
            self.evaluator.metrological_conformance_check(valid_fcf))

    def test_metrological_conformance_check_fail_missing_datum(self):
        invalid_fcf = """
        # FEATURES:
        #       - CONTROL(FORM) | TYPE(Text, Paragraph)
        #       - CONTROL(ORIENTATION) | TYPE(TONAL_CONSISTENCY) | DATUM(A)
        """
        self.assertFalse(
            self.evaluator.metrological_conformance_check(invalid_fcf))

    def test_metrological_conformance_check_fail_missing_control(self):
        invalid_fcf = """
        # DATUMS:
        #   A: ROLE(Strategic Integration Project Manager)
        # FEATURES:
        #       - CONTROL(FORM) | TYPE(Text, Paragraph)
        """
        self.assertFalse(
            self.evaluator.metrological_conformance_check(invalid_fcf))


if __name__ == '__main__':
    unittest.main()
