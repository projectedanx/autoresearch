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

    def test_calculate_geometric_density_score(self):
        # A fully connected graph of 4 nodes has 6 edges
        # GDS = edges / (nodes * (nodes - 1) / 2) = 6 / 6 = 1.0
        gds_full = self.evaluator.calculate_geometric_density_score(4, 6)
        self.assertAlmostEqual(gds_full, 1.0)

        # A sparse graph of 4 nodes with 1 edge
        # GDS = 1 / 6 = 0.1666...
        gds_sparse = self.evaluator.calculate_geometric_density_score(4, 1)
        self.assertAlmostEqual(gds_sparse, 0.16666666666666666)

        # 0 nodes or 1 node
        gds_zero = self.evaluator.calculate_geometric_density_score(0, 0)
        self.assertAlmostEqual(gds_zero, 0.0)

    def test_betti_loop_detect(self):
        self.assertFalse(self.evaluator.betti_loop_detect("Failure A"))
        self.assertFalse(self.evaluator.betti_loop_detect("Failure B"))
        # Repeating Failure A indicates a loop (Betti-1 > 0)
        self.assertTrue(self.evaluator.betti_loop_detect("Failure A"))

    def test_evaluate_hybrid_synergy_semantic_annihilation(self):
        result = self.evaluator.evaluate_hybrid_synergy(5.0, 5.0)
        self.assertEqual(result["status"], "Semantic Annihilation")
        self.assertEqual(result["human_weight"], 1.0)
        self.assertEqual(result["ai_weight"], 1.0)
        self.assertAlmostEqual(result["shear"], 0.0)

        # Within epsilon
        result = self.evaluator.evaluate_hybrid_synergy(
            5.0, 5.0 + (self.evaluator.epsilon / 2))
        self.assertEqual(result["status"], "Semantic Annihilation")

    def test_evaluate_hybrid_synergy_golden_scar_protocol(self):
        result = self.evaluator.evaluate_hybrid_synergy(2.0, 8.0)
        self.assertEqual(result["status"], "Golden Scar Protocol")
        self.assertEqual(result["human_weight"], 1.618)
        self.assertEqual(result["ai_weight"], 1.0)
        self.assertAlmostEqual(result["shear"], 6.0)

    def test_symbolic_scar_registry(self):
        from tactile_dialectician_simulation import SymbolicScarRegistry
        registry = SymbolicScarRegistry()
        registry.log_scar("Ontological mismatch", 1.618)
        self.assertEqual(len(registry.scars), 1)
        self.assertEqual(registry.scars[0]["scar"], "Ontological mismatch")
        self.assertEqual(registry.scars[0]["weight"], 1.618)

    def test_epistemic_escrow(self):
        from tactile_dialectician_simulation import EpistemicEscrow
        escrow = EpistemicEscrow()
        escrow.quarantine("Module_X", "[⊘] Mutually exclusive requirements")
        self.assertIn("Module_X", escrow.quarantined_modules)
        self.assertEqual(
            escrow.quarantined_modules["Module_X"],
            "[⊘] Mutually exclusive requirements")


if __name__ == '__main__':
    unittest.main()
