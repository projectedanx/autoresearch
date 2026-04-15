import unittest


class VULCANTopologyEvaluator:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.databases = set()

    def add_node(self, node_id: str, node_type: str, bounded_context: str):
        self.nodes[node_id] = {'type': node_type, 'context': bounded_context}
        if node_type == 'database':
            self.databases.add(node_id)

    def add_edge(self, source: str, target: str, interaction_type: str):
        self.edges.append({
            'source': source,
            'target': target,
            'interaction_type': interaction_type
        })

    def get_in_edges(self, target_node: str):
        return [edge for edge in self.edges if edge['target'] == target_node]

    def check_mereological_mandate(self) -> bool:
        """
        Rule 1: No transitivity fallacies.
        A microservice (Part) does not inherit the state or access rights of
        its cluster (Whole). Here we check that there are no transitivity
        violations where a node accesses another node's internal state
        directly without going through defined interfaces/events
        (simulated by checking edge attributes).
        """
        for edge in self.edges:
            u, v = edge['source'], edge['target']
            interaction = edge['interaction_type']
            if interaction not in ['api', 'event']:
                # Transitivity or improper access found
                if self.nodes[u]['context'] != self.nodes[v]['context']:
                    return False
        return True

    def check_shared_database_anathema(self) -> bool:
        """
        Rule 2: No Shared Database.
        Automatically reject any design that proposes multiple disparate
        bounded contexts writing directly to the same database tables.
        """
        for db in self.databases:
            writers_contexts = set()
            for edge in self.get_in_edges(db):
                u = edge['source']
                interaction = edge['interaction_type']
                # Ensure the interaction is a write/direct access
                if interaction in ['direct_write', 'direct_read_write']:
                    writers_contexts.add(self.nodes[u]['context'])
            if len(writers_contexts) > 1:
                return False
        return True

    def check_cfdi_brake(
            self,
            req_consistency: bool,
            req_availability: bool,
            req_partition_tolerance: bool) -> bool:
        """
        Rule 4: CAP Theorem violations (CFDI Brake).
        """
        if req_consistency and req_availability and req_partition_tolerance:
            return False  # Trigger CFDI Brake
        return True


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


if __name__ == '__main__':
    unittest.main()
