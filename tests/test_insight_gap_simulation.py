import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from insight_gap_simulation import InsightGapEvaluator

class TestInsightGapEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = InsightGapEvaluator()

    def test_interpretive_fracture(self):
        self.assertEqual(self.evaluator.check_interpretive_fracture(0.5), "SilentReasoning_Activated")
        self.assertEqual(self.evaluator.check_interpretive_fracture(0.3), "OK")

    def test_ssi(self):
        self.assertEqual(self.evaluator.check_ssi(0.05), "ContextLock_Executed")
        self.assertEqual(self.evaluator.check_ssi(0.02), "OK")

    def test_cfdi(self):
        self.assertEqual(self.evaluator.check_cfdi(0.20), "Quarantined_to_EpistemicEscrow")
        self.assertEqual(self.evaluator.check_cfdi(0.10), "OK")

    def test_routing(self):
        res1 = self.evaluator.route_request(0.2)
        self.assertEqual(res1["routing"], "System_1")
        self.assertEqual(res1["scaffold"], "Zero-Shot_Direct")

        res2 = self.evaluator.route_request(0.5)
        self.assertEqual(res2["routing"], "System_2")
        self.assertEqual(res2["scaffold"], "Least-to-Most_Stepwise_CoT")

    def test_process_telemetry(self):
        res = self.evaluator.process_telemetry(0.5, 0.05, 0.20)
        self.assertEqual(res["interpretive_fracture_status"], "SilentReasoning_Activated")
        self.assertEqual(res["ssi_status"], "ContextLock_Executed")
        self.assertEqual(res["cfdi_status"], "Quarantined_to_EpistemicEscrow")

if __name__ == '__main__':
    unittest.main()
