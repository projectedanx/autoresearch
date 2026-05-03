import unittest
from moe_simulation import MOETopologyEvaluator


class TestMOETopologyEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = MOETopologyEvaluator()

    def test_execute_petzold_sequence_success(self):
        input_semantic = "Please implement a highly robust and scalable cache."
        results = self.evaluator.execute_petzold_sequence(input_semantic)
        self.assertIn("THINK", results)
        self.assertIn("WRITE", results)
        self.assertIn("CODE", results)
        self.assertIn("REVIEW", results)
        self.assertEqual(self.evaluator.state_map["phase"], "RELEASED")

    def test_execute_petzold_sequence_vague_input(self):
        input_semantic = "Do task."
        with self.assertRaisesRegex(
                ValueError,
                "Input too vague. P1 Clarifier semantic lock failed."):
            self.evaluator.execute_petzold_sequence(input_semantic)

    def test_calculate_epistemic_drift(self):
        human_intent = [1.0, 0.5, 0.0]
        ai_execution = [0.9, 0.5, 0.1]
        drift = self.evaluator.calculate_epistemic_drift(
            human_intent, ai_execution)
        self.assertLess(drift, 0.1)

        bad_ai_execution = [0.0, 0.0, 1.0]
        bad_drift = self.evaluator.calculate_epistemic_drift(
            human_intent, bad_ai_execution)
        self.assertGreater(bad_drift, 0.1)

    def test_calculate_epistemic_drift_dimension_mismatch(self):
        human_intent = [1.0, 0.5]
        ai_execution = [0.9, 0.5, 0.1]
        with self.assertRaisesRegex(
                ValueError, "Vector dimensions must match."):
            self.evaluator.calculate_epistemic_drift(
                human_intent, ai_execution)

    def test_fuzzy_rcc8_spatial_bind(self):
        manifold_alpha = [0.1, 0.2, 0.1]
        manifold_beta = [0.2, 0.1, 0.1]
        # Max intersection for components:
        # max(0, 0.1+0.2-1) = 0
        # max(0, 0.2+0.1-1) = 0
        # max(0, 0.1+0.1-1) = 0
        # Total = 0 <= 0.15 -> True
        self.assertTrue(self.evaluator.fuzzy_rcc8_spatial_bind(
            manifold_alpha, manifold_beta))

        manifold_alpha_dense = [0.8, 0.9, 0.7]
        manifold_beta_dense = [0.7, 0.8, 0.6]
        # max(0, 0.8+0.7-1) = 0.5
        # Total = 0.5 + 0.7 + 0.3 = 1.5 > 0.15 -> False
        self.assertFalse(self.evaluator.fuzzy_rcc8_spatial_bind(
            manifold_alpha_dense, manifold_beta_dense))


if __name__ == '__main__':
    unittest.main()
