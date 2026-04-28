import unittest
import math
from pluriversal_simulation import PluriversalTopologyEvaluator


class TestPluriversalTopologyEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = PluriversalTopologyEvaluator()

    def test_anionic_masking(self):
        logits = [0.1, 0.5, 2.0, -1.0, 3.5]
        forbidden_indices = {1, 4}
        masked = self.evaluator.anionic_logit_masking(
            logits, forbidden_indices)
        self.assertEqual(masked[0], 0.1)
        self.assertTrue(math.isinf(masked[1]) and masked[1] < 0)
        self.assertEqual(masked[2], 2.0)
        self.assertEqual(masked[3], -1.0)
        self.assertTrue(math.isinf(masked[4]) and masked[4] < 0)

    def test_epistemic_escrow(self):
        schema1 = {"type": "A"}
        schema2 = {"type": "B"}
        self.evaluator.add_to_epistemic_escrow(
            "auth_schema", [schema1, schema2])
        self.assertIn("auth_schema", self.evaluator.epistemic_escrow)

        auth_len = len(self.evaluator.epistemic_escrow["auth_schema"])
        self.assertEqual(auth_len, 2)

        resolved = {"type": "C"}
        result = self.evaluator.resolve_epistemic_escrow(
            "auth_schema", resolved)
        self.assertEqual(result, resolved)
        self.assertNotIn("auth_schema", self.evaluator.epistemic_escrow)

    def test_rcc8_fencing(self):
        self.evaluator.set_rcc8_relation("local_db", "global_auth", "DC")
        self.assertFalse(self.evaluator.check_rcc8_fencing(
            "local_db", "global_auth"))

        self.evaluator.set_rcc8_relation("cache", "app", "EC")
        self.assertTrue(self.evaluator.check_rcc8_fencing("cache", "app"))

        with self.assertRaises(ValueError):
            self.evaluator.set_rcc8_relation("x", "y", "INVALID")

    def test_betti_numbers(self):
        # Two disconnected components, one with a cycle, one without
        graph = {
            "A": ["B", "C"],
            "B": ["A", "C"],
            "C": ["A", "B", "D"],
            "D": ["C"],
            "E": ["F"],
            "F": ["E"]
        }
        b0, b1 = self.evaluator.calculate_betti_numbers(graph)
        self.assertEqual(b0, 2)
        self.assertEqual(b1, 1)

    def test_cfdi_brake(self):
        # High confidence, low validity -> high divergence -> brake
        self.assertTrue(self.evaluator.evaluate_cfdi_brake(
            0.95, 0.10, threshold=0.8))
        self.assertEqual(len(self.evaluator.scar_registry), 1)

        # Low divergence -> no brake
        self.assertFalse(self.evaluator.evaluate_cfdi_brake(
            0.80, 0.85, threshold=0.8))
        self.assertEqual(len(self.evaluator.scar_registry), 1)

        # NaN handling -> max divergence -> brake
        self.assertTrue(self.evaluator.evaluate_cfdi_brake(
            float('nan'), 0.5, threshold=0.8))
        self.assertEqual(len(self.evaluator.scar_registry), 2)


if __name__ == '__main__':
    unittest.main()
