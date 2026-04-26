import collections


class VANCETopologyEvaluator:
    """
    Simulates the VANCE - Vector-Anchored Node & Context Engineer agent.
    Implements Betti-1 cycle detection, the Nitinol Failure Ledger (NFL),
    Draft-Conditioned Constrained Decoder (DCCD) schema guards,
    and Mereological bounding checks.
    """

    def __init__(self):
        self.scars = []  # Nitinol Failure Ledger (NFL)
        self.edges = collections.defaultdict(list)  # Optimizing edge lookups
        self.nodes = {}

    def add_node(self, node_id, uri, scope_depth=0, node_type="Symbol"):
        self.nodes[node_id] = {
            "uri": uri,
            "scope_depth": scope_depth,
            "type": node_type
        }

    def add_edge(self, source, target, edge_type):
        """
        Adds a directed edge.
        Using collections.defaultdict(list) grouping by source node.
        """
        self.edges[source].append({"target": target, "type": edge_type})

    def detect_betti_1_cycle(self):
        """
        Detects circular dependencies in the IMPORTS graph using DFS.
        """
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)

            for edge in self.edges.get(node, []):
                if edge["type"] == "IMPORTS":
                    target = edge["target"]
                    if target not in visited:
                        if dfs(target):
                            return True
                    elif target in rec_stack:
                        return True

            rec_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited:
                if dfs(node):
                    return True
        return False

    def check_mereological_bounds(self, source, target):
        """
        Enforces transitivity check via SCOPES_WITHIN edge chain.
        Returns True if a valid path exists, False otherwise.
        """
        visited = set()

        def dfs(node):
            if node == target:
                return True
            visited.add(node)
            for edge in self.edges.get(node, []):
                if edge["type"] == "SCOPES_WITHIN":
                    next_node = edge["target"]
                    if next_node not in visited:
                        if dfs(next_node):
                            return True
            return False

        return dfs(source)

    def record_scar(self, scar_id, trigger, violation):
        """
        Adds an entry to the Nitinol Failure Ledger.
        """
        self.scars.append({
            "scar_id": scar_id,
            "trigger": trigger,
            "violation": violation
        })

    def dccd_guard(self, payload, required_fields):
        """
        Draft-Conditioned Constrained Decoder schema validation.
        Validates the payload against required fields.
        Returns (True, None) if valid, (False, reason) if invalid.
        """
        for field in required_fields:
            if field not in payload:
                # Instead of emitting, we reject
                violation = f"Missing required field: {field}"
                self.record_scar(
                    f"SCAR_{len(self.scars)}", "schema_validation", violation)
                return False, violation
        return True, None
