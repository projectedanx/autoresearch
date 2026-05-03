import unittest
from vulcan_simulation import VULCANTopologyEvaluator


class TestVULCANRules(unittest.TestCase):
    def test_mereological_mandate_pass(self):
        evaluator = VULCANTopologyEvaluator()
        evaluator.add_node('svc_a', 'service', 'context_a')
        evaluator.add_node('svc_b', 'service', 'context_b')
        evaluator.add_edge('svc_a', 'svc_b', 'api')
        self.assertTrue(evaluator.check_mereological_mandate())

    def test_mereological_mandate_fail(self):
        evaluator = VULCANTopologyEvaluator()
        evaluator.add_node('svc_a', 'service', 'context_a')
        evaluator.add_node('svc_b', 'service', 'context_b')
        evaluator.add_edge('svc_a', 'svc_b', 'direct_memory_access')
        self.assertFalse(evaluator.check_mereological_mandate())

    def test_shared_database_anathema_pass(self):
        evaluator = VULCANTopologyEvaluator()
        evaluator.add_node('svc_a', 'service', 'context_a')
        evaluator.add_node('db_a', 'database', 'context_a')
        evaluator.add_node('svc_b', 'service', 'context_b')
        evaluator.add_node('db_b', 'database', 'context_b')
        evaluator.add_edge('svc_a', 'db_a', 'direct_read_write')
        evaluator.add_edge('svc_b', 'db_b', 'direct_read_write')
        self.assertTrue(evaluator.check_shared_database_anathema())

    def test_shared_database_anathema_fail(self):
        evaluator = VULCANTopologyEvaluator()
        evaluator.add_node('svc_a', 'service', 'context_a')
        evaluator.add_node('svc_b', 'service', 'context_b')
        evaluator.add_node('db_shared', 'database', 'shared_infra')
        evaluator.add_edge('svc_a', 'db_shared', 'direct_read_write')
        evaluator.add_edge('svc_b', 'db_shared', 'direct_write')
        self.assertFalse(evaluator.check_shared_database_anathema())

    def test_cfdi_brake_pass(self):
        evaluator = VULCANTopologyEvaluator()
        # AP system
        self.assertTrue(evaluator.check_cfdi_brake(False, True, True))
        # CP system
        self.assertTrue(evaluator.check_cfdi_brake(True, False, True))

    def test_cfdi_brake_fail(self):
        evaluator = VULCANTopologyEvaluator()
        # CAP violated
        self.assertFalse(evaluator.check_cfdi_brake(True, True, True))

    def test_evaluate_nfr_gate(self):
        evaluator = VULCANTopologyEvaluator()
        # Any true should return Microservice Decomposition
        self.assertEqual(evaluator.evaluate_nfr_gate(
            True, False, False, False), "Microservice Decomposition")
        self.assertEqual(evaluator.evaluate_nfr_gate(
            False, True, False, False), "Microservice Decomposition")
        self.assertEqual(evaluator.evaluate_nfr_gate(
            False, False, True, False), "Microservice Decomposition")
        self.assertEqual(evaluator.evaluate_nfr_gate(
            False, False, False, True), "Microservice Decomposition")
        # All false should return Modular Monolith
        self.assertEqual(evaluator.evaluate_nfr_gate(
            False, False, False, False), "Modular Monolith")

    def test_analyze_blast_radius(self):
        evaluator = VULCANTopologyEvaluator()
        evaluator.add_node('svc_a', 'service', 'context_a')
        evaluator.add_node('svc_b', 'service', 'context_b')
        evaluator.add_node('svc_c', 'service', 'context_c')
        evaluator.add_node('svc_d', 'service', 'context_d')
        evaluator.add_node('db_main', 'database', 'shared')

        # 4 edges, db_main has 3 in-edges (75% blast radius)
        evaluator.add_edge('svc_a', 'db_main', 'api')
        evaluator.add_edge('svc_b', 'db_main', 'api')
        evaluator.add_edge('svc_c', 'db_main', 'api')
        evaluator.add_edge('svc_c', 'svc_d', 'api')

        flagged = evaluator.analyze_blast_radius()
        self.assertIn('db_main', flagged)

        # svc_d has 1 in-edge, 1/4 = 0.25 > 0.20, so it should be flagged
        self.assertIn('svc_d', flagged)
        self.assertEqual(len(flagged), 2)

    def test_analyze_blast_radius_no_edges(self):
        evaluator = VULCANTopologyEvaluator()
        evaluator.add_node('svc_a', 'service', 'context_a')
        self.assertEqual(evaluator.analyze_blast_radius(), [])


if __name__ == '__main__':
    unittest.main()
