import unittest
from viper_simulation import VIPERTopologyEvaluator


class TestVIPEREvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = VIPERTopologyEvaluator()

    def test_calculate_ads(self):
        # 2 adjectives, 6 nouns -> 2/6 = 0.33
        text = "The old woman wore a dark coat in the cafe interior with walls and floor."  # noqa: E501
        ads = self.evaluator.calculate_ads(text)
        self.assertAlmostEqual(ads, 0.3333333, places=5)

    def test_apply_banned_token_protocol(self):
        text = "This is a beautiful and cinematic masterpiece."
        rejected = self.evaluator.apply_banned_token_protocol(text)
        self.assertIn("beautiful", rejected)
        self.assertIn("cinematic", rejected)
        self.assertIn("masterpiece", rejected)
        self.assertEqual(len(rejected), 3)

    def test_validate_hgi(self):
        # Valid HGI
        hfp_valid = "+++HardwareForcedPhysicality(Lens='50mm', Aperture='T1.4', Lighting='Key light')"  # noqa: E501
        self.assertTrue(self.evaluator.validate_hgi(hfp_valid))

        # Missing Lighting
        hfp_invalid = "+++HardwareForcedPhysicality(Lens='50mm', Aperture='T1.4')"  # noqa: E501
        self.assertFalse(self.evaluator.validate_hgi(hfp_invalid))

    def test_enforce_spatial_bind(self):
        subjects = ["Woman", "Umbrella"]
        bindings = self.evaluator.enforce_spatial_bind(subjects)
        self.assertEqual(len(bindings), 1)
        self.assertIn("Subject_A='Woman'", bindings[0])

    def test_petzold_sequence_progression(self):
        self.assertEqual(self.evaluator.state, "THINK")
        self.evaluator.advance_state("DENOISE")
        self.assertEqual(self.evaluator.state, "DENOISE")
        self.evaluator.advance_state("PHYSICALIZE")
        self.assertEqual(self.evaluator.state, "PHYSICALIZE")
        self.evaluator.advance_state("EXTRUDE")
        self.assertEqual(self.evaluator.state, "EXTRUDE")

    def test_petzold_sequence_invalid_progression(self):
        with self.assertRaises(ValueError):
            self.evaluator.advance_state("EXTRUDE")  # From THINK, invalid

    def test_process_prompt_success(self):
        # 0 adjectives, 2 nouns -> 0.0 ADS
        text = "A woman in a cafe."
        result = self.evaluator.process_prompt(text)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["OSM"]["ADS_Final"], 0.0)

    def test_process_prompt_halt_ads(self):
        # 6 adjectives, 1 noun -> 6.0 ADS (High)
        text = "An old dark heavy nicotine-stained single condensation-streaked woman."  # noqa: E501
        result = self.evaluator.process_prompt(text)
        self.assertEqual(result["status"], "HALT")
        self.assertIn("ADS post-strip > 0.15", result["reason"])


if __name__ == '__main__':
    unittest.main()
