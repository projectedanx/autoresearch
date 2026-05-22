import unittest
from lexicon_simulation import PDLLexiconEvaluator


class TestLexiconSimulation(unittest.TestCase):
    def setUp(self):
        self.evaluator = PDLLexiconEvaluator()

    def test_saponification_paradox(self):
        # PAT-007 Lexical Saponification Paradox
        w0 = 1.0
        # common epistemic term lambda
        lambda_rate = 0.23

        # After 0 uses
        w_0 = self.evaluator.calculate_saponification_weight(
            w0, lambda_rate, 0)
        self.assertAlmostEqual(w_0, 1.0)
        self.assertFalse(self.evaluator.check_saponification_onset(w0, w_0))

        # After 1 use
        w_1 = self.evaluator.calculate_saponification_weight(
            w0, lambda_rate, 1)
        # 1 - w_1 approx 0.205
        self.assertTrue(self.evaluator.check_saponification_onset(w0, w_1))

        # Empirical Data: 'Isomorphism' -> 34% drop after 4 uses
        # (need custom lambda if specific, let's test lambda=0.104)
        w_4 = self.evaluator.calculate_saponification_weight(w0, 0.104, 4)
        drop = 1 - w_4
        self.assertAlmostEqual(drop, 0.34, places=2)

    def test_workflow_narrowing_effect(self):
        # PAT-003 Workflow Narrowing Effect
        w0 = 1.0

        # N=2, no context lock
        w_2 = self.evaluator.simulate_workflow_narrowing(w0, 2, False)
        self.assertEqual(w_2, 1.0)

        # N=4, no context lock (degradation onset)
        w_4 = self.evaluator.simulate_workflow_narrowing(w0, 4, False)
        self.assertEqual(w_4, 0.8)
        self.assertFalse(
            self.evaluator.check_workflow_narrowing_collapse(w0, w_4))

        # N=6, no context lock (catastrophic collapse)
        w_6 = self.evaluator.simulate_workflow_narrowing(w0, 6, False)
        self.assertEqual(w_6, 0.45)
        self.assertTrue(
            self.evaluator.check_workflow_narrowing_collapse(w0, w_6))

        # N=6, WITH context lock
        w_6_locked = self.evaluator.simulate_workflow_narrowing(w0, 6, True)
        self.assertEqual(w_6_locked, 1.0)
        self.assertFalse(
            self.evaluator.check_workflow_narrowing_collapse(w0, w_6_locked))

    def test_polyglot_hallucination_resonance(self):
        # PAT-005 Polyglot Hallucination Resonance

        # Phronesis Index Φ >= 0.05 AND CFDI <= 0.15 -> False
        self.assertFalse(
            self.evaluator.check_polyglot_hallucination_resonance(0.08, 0.10))

        # Phronesis Index Φ < 0.05 -> True
        self.assertTrue(
            self.evaluator.check_polyglot_hallucination_resonance(0.04, 0.10))

        # CFDI > 0.15 -> True
        self.assertTrue(
            self.evaluator.check_polyglot_hallucination_resonance(0.08, 0.20))

    def test_productivity_j_curve(self):
        # Time t=0
        score_0 = self.evaluator.simulate_productivity_j_curve(0.0)
        self.assertEqual(score_0, 0.5)  # 1.0 - 0.5 + 0.0

        # Time t=1.0 (friction dip is e^-1 * 0.5 = 0.183,
        # gain = 1.2 * 1 / 10 = 0.12)
        score_1 = self.evaluator.simulate_productivity_j_curve(
            1.0)
        self.assertAlmostEqual(score_1, 1.0 - 0.1839 + 0.12, places=2)

        # Time t=10.0 (high efficiency gain)
        score_10 = self.evaluator.simulate_productivity_j_curve(10.0)
        self.assertGreater(score_10, 10.0)

    def test_paraconsistent_tension(self):
        # Tension < 1.0
        self.assertAlmostEqual(
            self.evaluator.compute_paraconsistent_tension(0.8, 0.5), 0.3)

        # Tension > 1.0 -> Golden Scar Constraint (1.618)
        self.assertEqual(
            self.evaluator.compute_paraconsistent_tension(2.0, 0.5), 1.618)

    def test_agentic_inversion_engine(self):
        # Drift within threshold
        drift, leap = self.evaluator.calculate_epistemic_drift_and_leap(
            0.8, 0.5, 0.5)
        self.assertAlmostEqual(drift, 0.3)
        self.assertFalse(leap)

        # Drift exceeds threshold
        drift, leap = self.evaluator.calculate_epistemic_drift_and_leap(
            1.2, 0.5, 0.5)
        self.assertAlmostEqual(drift, 0.7)
        self.assertTrue(leap)

    def test_lexical_cartography(self):
        hasse_edges = [
            ("nodeA", "semantic_drift"),
            ("nodeB", "connotation_vectors"),
            ("nodeC", "ambiguity_zones"),
            ("nodeD", "semantic_drift")
        ]

        # Normal targets
        targets = {'semantic_drift', 'connotation_vectors'}
        result = self.evaluator.process_lexical_cartography(
            hasse_edges, targets)
        self.assertEqual(set(result['semantic_drift']), {'nodeA', 'nodeD'})
        self.assertEqual(
            set(result['connotation_vectors']), {'nodeB'})
        self.assertNotIn('ambiguity_zones', result)

        # Blind spot target -> Exception
        with self.assertRaises(ValueError):
            self.evaluator.process_lexical_cartography(
                hasse_edges, {'semiotic_blind_spots'})


if __name__ == '__main__':
    unittest.main()
