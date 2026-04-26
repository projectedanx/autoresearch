import unittest
from whimsy_simulation import WhimsyTopologyEvaluator


class TestWhimsyTopologyEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = WhimsyTopologyEvaluator()

    def test_manifold_separation_pass(self):
        # Only Manifold Alpha (copy.json) modified
        commits_alpha = [{"file": "copy.json"}]
        self.assertTrue(
            self.evaluator.check_manifold_separation(commits_alpha))

        # Only Manifold Beta (component.css) modified
        commits_beta = [{"file": "component.css"}]
        self.assertTrue(self.evaluator.check_manifold_separation(commits_beta))

    def test_manifold_separation_fail(self):
        # Both modified simultaneously -> violation
        commits_mixed = [{"file": "copy.json"}, {"file": "component.css"}]
        self.assertFalse(
            self.evaluator.check_manifold_separation(commits_mixed))

    def test_calculate_cfdi(self):
        # cosine_sim=0.9, entropy=1.0 -> cfdi=0.1
        cfdi = self.evaluator.calculate_cfdi(0.9, 1.0)
        self.assertAlmostEqual(cfdi, 0.1)

        # zero entropy test -> max divergence
        cfdi_zero_entropy = self.evaluator.calculate_cfdi(1.0, 0.0)
        self.assertEqual(cfdi_zero_entropy, 1.0)

    def test_check_cfdi_threshold(self):
        # < 0.15 passes
        self.assertTrue(self.evaluator.check_cfdi_threshold(0.14))
        # >= 0.15 fails
        self.assertFalse(self.evaluator.check_cfdi_threshold(0.15))
        self.assertFalse(self.evaluator.check_cfdi_threshold(0.20))

    def test_classify_whimsy_zone(self):
        self.assertEqual(self.evaluator.classify_whimsy_zone(
            "HARD_LOCKOUT")["allowed"], "none")
        self.assertEqual(self.evaluator.classify_whimsy_zone(
            "RESTRICTED")["allowed"], "micro_animation_only")
        self.assertEqual(self.evaluator.classify_whimsy_zone(
            "CONDITIONAL")["allowed"], "warm_directive_copy")
        self.assertEqual(self.evaluator.classify_whimsy_zone(
            "OPEN")["allowed"], "full_latitude")

    def test_scar_proximity_search(self):
        self.evaluator.add_symbolic_scar(
            "SCAR-001", ["payment", "high_anxiety"], "confusion")

        # Overlapping tags
        self.assertTrue(self.evaluator.scar_proximity_search(
            ["payment", "checkout"]))
        # Non-overlapping tags
        self.assertFalse(self.evaluator.scar_proximity_search(
            ["loading_screen", "onboarding"]))


if __name__ == '__main__':
    unittest.main()
