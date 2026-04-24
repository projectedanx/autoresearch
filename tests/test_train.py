import unittest
import train


class TestTrain(unittest.TestCase):
    def test_get_lr_multiplier(self):
        # Save original values
        orig_warmup = train.WARMUP_RATIO
        orig_warmdown = train.WARMDOWN_RATIO
        orig_final_lr = train.FINAL_LR_FRAC

        try:
            # Case 1: Standard case with 0.1 warmup, 0.2 warmdown
            train.WARMUP_RATIO = 0.1
            train.WARMDOWN_RATIO = 0.2
            train.FINAL_LR_FRAC = 0.05

            # Warmup phase (progress < WARMUP_RATIO)
            self.assertEqual(train.get_lr_multiplier(0.0), 0.0)
            self.assertAlmostEqual(train.get_lr_multiplier(0.05), 0.5)

            # Steady phase (WARMUP_RATIO <= progress < 1.0 - WARMDOWN_RATIO)
            self.assertEqual(train.get_lr_multiplier(0.1), 1.0)
            self.assertEqual(train.get_lr_multiplier(0.5), 1.0)
            self.assertEqual(train.get_lr_multiplier(0.79), 1.0)

            # Warmdown phase (progress >= 1.0 - WARMDOWN_RATIO)
            # When progress = 0.8, cooldown = (1.0 - 0.8) / 0.2 = 1.0
            # multiplier = 1.0 * 1.0 + 0.0 * 0.05 = 1.0
            self.assertAlmostEqual(train.get_lr_multiplier(0.8), 1.0)

            # When progress = 0.9, cooldown = (1.0 - 0.9) / 0.2 = 0.5
            # multiplier = 0.5 * 1.0 + 0.5 * 0.05 = 0.525
            self.assertAlmostEqual(train.get_lr_multiplier(0.9), 0.525)

            # When progress = 1.0, cooldown = 0.0
            # multiplier = 0.0 * 1.0 + 1.0 * 0.05 = 0.05
            self.assertAlmostEqual(train.get_lr_multiplier(1.0), 0.05)

            # Case 2: Zero warmup
            train.WARMUP_RATIO = 0.0
            train.WARMDOWN_RATIO = 0.5
            train.FINAL_LR_FRAC = 0.0

            self.assertEqual(train.get_lr_multiplier(0.0), 1.0)
            self.assertEqual(train.get_lr_multiplier(0.2), 1.0)
            self.assertEqual(train.get_lr_multiplier(0.49), 1.0)

            # When progress = 0.5, cooldown = 1.0
            self.assertAlmostEqual(train.get_lr_multiplier(0.5), 1.0)
            # When progress = 0.75, cooldown = 0.5
            self.assertAlmostEqual(train.get_lr_multiplier(0.75), 0.5)
            # When progress = 1.0, cooldown = 0.0
            self.assertAlmostEqual(train.get_lr_multiplier(1.0), 0.0)

        finally:
            # Restore original values
            train.WARMUP_RATIO = orig_warmup
            train.WARMDOWN_RATIO = orig_warmdown
            train.FINAL_LR_FRAC = orig_final_lr

    def test_has_ve(self):
        # Case 1: Even n_layer (e.g., 12)
        # (12 - 1) % 2 = 1. So odd layer_idx should return True.
        self.assertFalse(train.has_ve(0, 12))
        self.assertTrue(train.has_ve(1, 12))
        self.assertFalse(train.has_ve(2, 12))
        self.assertTrue(train.has_ve(11, 12))

        # Case 2: Odd n_layer (e.g., 13)
        # (13 - 1) % 2 = 0. So even layer_idx should return True.
        self.assertTrue(train.has_ve(0, 13))
        self.assertFalse(train.has_ve(1, 13))
        self.assertTrue(train.has_ve(2, 13))
        self.assertTrue(train.has_ve(12, 13))

        # Case 3: n_layer = 1
        # (1 - 1) % 2 = 0.
        self.assertTrue(train.has_ve(0, 1))


if __name__ == '__main__':
    unittest.main()
