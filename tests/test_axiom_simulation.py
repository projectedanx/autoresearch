import unittest
from axiom_simulation import AxiomTopologyEvaluator


class TestAxiomSimulation(unittest.TestCase):
    def setUp(self):
        self.evaluator = AxiomTopologyEvaluator()

    def test_log_symbolic_scar(self):
        scar_id = self.evaluator.log_symbolic_scar(
            trigger="Missing token",
            failure_mode="401 Unauthorized",
            prevention_directive="Include token in header"
        )
        self.assertEqual(len(self.evaluator.scar_registry), 1)
        self.assertEqual(scar_id, "SSR-20260315-001")
        self.assertEqual(
            self.evaluator.scar_registry[0]["trigger"], "Missing token"
        )

    def test_check_anionic_veto(self):
        # Should pass
        self.assertTrue(self.evaluator.check_anionic_veto(
            "The system is highly tested and verified."
        ))
        # Should fail due to "seamless"
        self.assertFalse(self.evaluator.check_anionic_veto(
            "This provides a seamless integration."
        ))
        # Should fail due to "cutting-edge"
        self.assertFalse(self.evaluator.check_anionic_veto(
            "This is a cutting-edge solution."
        ))

    def test_calculate_sds(self):
        text = "This is a ten word sentence to test the function"
        # 10 words, 1 filler word -> 1 - (1/10) = 0.9
        self.assertAlmostEqual(self.evaluator.calculate_sds(text, 1), 0.9)

    def test_calculate_ssi(self):
        text = "This is a ten word sentence to test the function"
        # 10 words, 1 forbidden match -> 1/10 = 0.1
        self.assertAlmostEqual(self.evaluator.calculate_ssi(text, 1), 0.1)

    def test_evaluate_epistemic_escrow(self):
        self.assertTrue(self.evaluator.evaluate_epistemic_escrow(0.10))
        self.assertFalse(self.evaluator.evaluate_epistemic_escrow(0.20))

    def test_check_semantic_drift(self):
        self.assertTrue(self.evaluator.check_semantic_drift(0.10))
        self.assertFalse(self.evaluator.check_semantic_drift(0.30))

    def test_simulate_dccd_generation_success(self):
        result = self.evaluator.simulate_dccd_generation(
            draft_text="This is a perfectly normal and acceptable "
                       "sentence of exactly ten words",
            filler_count=1,      # SDS: 1 - 1/12 = 0.916... > 0.85
            forbidden_count=0,   # SSI: 0 < 0.05
            cfdi=0.10,           # < 0.15
            drift_distance=0.10  # < 0.22
        )
        self.assertEqual(result["status"], "PASS")

    def test_simulate_dccd_generation_epistemic_escrow_failure(self):
        with self.assertRaisesRegex(
            ValueError, "EPISTEMIC_ESCROW TRIGGERED"
        ):
            self.evaluator.simulate_dccd_generation(
                draft_text="Valid text", filler_count=0, forbidden_count=0,
                cfdi=0.20, drift_distance=0.10
            )

    def test_simulate_dccd_generation_drift_failure(self):
        with self.assertRaisesRegex(
            ValueError, "Semantic Drift exceeded"
        ):
            self.evaluator.simulate_dccd_generation(
                draft_text="Valid text", filler_count=0, forbidden_count=0,
                cfdi=0.10, drift_distance=0.30
            )

    def test_simulate_dccd_generation_ssi_failure(self):
        # 4 words, 1 forbidden -> SSI 0.25 >= 0.05
        with self.assertRaisesRegex(
            ValueError, "SSI threshold breached"
        ):
            self.evaluator.simulate_dccd_generation(
                draft_text="Seamlessly integrate the system", filler_count=0,
                forbidden_count=1, cfdi=0.10, drift_distance=0.10
            )

    def test_simulate_dccd_generation_sds_failure(self):
        # 10 words, 2 fillers -> SDS 1 - 0.2 = 0.8 <= 0.85
        with self.assertRaisesRegex(ValueError, "SDS below 0.85"):
            self.evaluator.simulate_dccd_generation(
                draft_text="I am happy to help you with this "
                           "particular issue",
                filler_count=2, forbidden_count=0, cfdi=0.10,
                drift_distance=0.10
            )


if __name__ == '__main__':
    unittest.main()
