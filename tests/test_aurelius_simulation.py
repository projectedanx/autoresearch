import unittest
import torch
from aurelius_simulation import ProjectAureliusEvaluator


class TestProjectAureliusEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = ProjectAureliusEvaluator(
            latent_dim=128, phantom_dims=32
        )

    def test_modulate_phantom_dimensions(self):
        # Test Hyperbolic
        out_hyperbolic = self.evaluator.modulate_phantom_dimensions(
            "hyperbolic", curvature=-0.5
        ).clone()
        self.assertEqual(out_hyperbolic.shape[0], 160)

        # Test Spherical
        out_spherical = self.evaluator.modulate_phantom_dimensions(
            "spherical", curvature=0.5
        ).clone()
        self.assertEqual(out_spherical.shape[0], 160)

        # They should diverge due to different modulations
        self.assertFalse(
            torch.allclose(out_hyperbolic[-32:], out_spherical[-32:])
        )

    def test_autonomous_prompt_optimization(self):
        prompt = "A hyper-realistic dodecahedron"
        opt_prompt, score = self.evaluator.autonomous_prompt_optimization(
            prompt, iterations=5
        )

        self.assertTrue("optimized" in opt_prompt)
        self.assertGreater(score, 0.5)

    def test_dynamic_provenance_tracking(self):
        t_ids = ["data_A", "data_B", "data_C"]
        initial_weights = torch.tensor([0.33, 0.33, 0.34], dtype=torch.float32)

        # Force data_A to be over-represented
        self.evaluator.provenance_weights["data_A"] = 2.0

        adj_weights, drift = self.evaluator.dynamic_provenance_tracking(
            t_ids, initial_weights
        )

        self.assertEqual(adj_weights.shape, initial_weights.shape)
        # Verify normalization
        torch.testing.assert_close(adj_weights.sum(), torch.tensor(1.0))
        # data_A should be penalized relative to others
        self.assertLess(adj_weights[0].item(), adj_weights[2].item())

    def test_generate_hyper_spectral_hdri(self):
        wavelengths = [450.0, 500.0, 550.0, 600.0, 650.0]
        spectral_data = self.evaluator.generate_hyper_spectral_hdri(
            wavelengths
        )

        self.assertEqual(len(spectral_data), len(wavelengths))
        # 550 should be the peak
        self.assertEqual(torch.argmax(spectral_data).item(), 2)


if __name__ == "__main__":
    unittest.main()
