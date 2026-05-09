import unittest
from vortex_architect_simulation import VortexArchitectEvaluator


class TestVortexArchitectSimulation(unittest.TestCase):
    def setUp(self):
        self.evaluator = VortexArchitectEvaluator()

    def test_detect_betti_1_loop_pass(self):
        # Provide a trace with the cycle: updating, failing, reverting, updating, failing, reverting  # noqa: E501
        trace = ['start', 'updating', 'failing', 'reverting',
                 'updating', 'failing', 'reverting', 'end']
        self.assertTrue(self.evaluator.detect_betti_1_loop(trace))

    def test_detect_betti_1_loop_fail(self):
        # Provide a trace without the consecutive cycle
        trace = ['start', 'updating', 'failing',
                 'reverting', 'updating', 'success', 'end']
        self.assertFalse(self.evaluator.detect_betti_1_loop(trace))

    def test_check_semantic_mutex_locking_pass(self):
        # Disjoint resources
        agent_processes = {
            'agent_1': ['file1', 'file2'],
            'agent_2': ['file3', 'file4']
        }
        self.assertTrue(
            self.evaluator.check_semantic_mutex_locking(agent_processes))

    def test_check_semantic_mutex_locking_fail(self):
        # Overlapping resources
        agent_processes = {
            'agent_1': ['file1', 'file2'],
            'agent_2': ['file2', 'file3']
        }
        self.assertFalse(
            self.evaluator.check_semantic_mutex_locking(agent_processes))

    def test_evaluate_pal2v(self):
        phi = 1.618

        # Conflict A is dominant
        res_a, res_b = self.evaluator.evaluate_pal2v(10.0, 5.0)
        self.assertAlmostEqual(res_a, 10.0 * phi)
        self.assertAlmostEqual(res_b, 5.0 * 1.0)

        # Conflict B is dominant
        res_a, res_b = self.evaluator.evaluate_pal2v(3.0, 8.0)
        self.assertAlmostEqual(res_a, 3.0 * 1.0)
        self.assertAlmostEqual(res_b, 8.0 * phi)

        # Equal
        res_a, res_b = self.evaluator.evaluate_pal2v(7.0, 7.0)
        self.assertAlmostEqual(res_a, 7.0 * phi)
        self.assertAlmostEqual(res_b, 7.0 * 1.0)


if __name__ == '__main__':
    unittest.main()
