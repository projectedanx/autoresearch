import unittest
from collections import defaultdict


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
        # Group edges by target for O(E) edge retrieval
        edges_by_target = defaultdict(list)
        for edge in self.edges:
            edges_by_target[edge['target']].append(edge)

        for db in self.databases:
            writers_contexts = set()
            for edge in edges_by_target[db]:
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

    def evaluate_nfr_gate(
            self,
            diff_scale: bool,
            diff_deploy_cadence: bool,
            diff_team: bool,
            require_failure_isolation: bool) -> str:
        """
        Rule 3: No Unwarranted Complexity (Bricolage Lens).
        """
        cond = (diff_scale or diff_deploy_cadence or diff_team or
                require_failure_isolation)
        if cond:
            return "Microservice Decomposition"
        else:
            return "Modular Monolith"

    def analyze_blast_radius(self) -> list:
        """
        Phase 3: DAG (Topology Mapping).
        Compute blast radius for each node based on in-degree.
        Flag nodes with blast radius > 20% of total functionality.
        Assume total functionality represented by total number of edges.
        """
        total_edges = len(self.edges)
        if total_edges == 0:
            return []

        flagged_nodes = []
        edges_by_target = defaultdict(list)
        for edge in self.edges:
            edges_by_target[edge['target']].append(edge)

        for node_id in self.nodes:
            in_degree = len(edges_by_target[node_id])
            blast_radius = in_degree / total_edges
            if blast_radius > 0.20:
                flagged_nodes.append(node_id)

        return flagged_nodes


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
