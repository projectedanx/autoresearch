import re
from typing import List, Dict


class CIPHERTopologyEvaluator:
    def __init__(self):
        self.current_phase = "IDLE"
        self.phases = ["THINK", "THREAT_MODEL", "AUDIT", "REPORT"]
        self.mereological_edges = []
        self.nodes = {}

        # Autonymic Isolate definitions
        self.forbidden_patterns = {
            "SQLI_PATTERN_CWE89": r"(?i)union\s+select|waitfor\s+delay",
            "XSS_PATTERN_CWE79": r"(?i)<script>|javascript:",
            "PATH_TRAVERSAL_CWE22": r"\.\./\.\./",
        }

    def set_phase(self, phase: str):
        if phase not in self.phases and phase != "IDLE":
            raise ValueError(f"Invalid PetzoldSequence phase: {phase}")
        self.current_phase = phase

    def enforce_petzold_sequence(self, attempted_action: str) -> bool:
        """
        Rule: block_code_generation_until_phase="AUDIT"
        """
        if attempted_action == "CODE_GENERATION" and \
                self.current_phase not in ["AUDIT", "REPORT"]:
            raise ValueError(
                f"Interpretive Fracture Prevented: Cannot execute "
                f"{attempted_action} during {self.current_phase} phase."
            )
        return True

    def add_node(self, node_id: str, node_type: str, component: str):
        self.nodes[node_id] = {'type': node_type, 'component': component}

    def add_trust_edge(self, source: str, target: str):
        self.mereological_edges.append({'source': source, 'target': target})

    def check_mereology_route(self) -> bool:
        """
        CONSTRAINT: A frontend component MUST NOT have a trust relationship
        path to a backend data store.
        """
        for edge in self.mereological_edges:
            source = self.nodes.get(edge['source'])
            target = self.nodes.get(edge['target'])

            if not source or not target:
                continue

            if source['type'] == 'frontend' and target['type'] == 'database':
                raise ValueError(
                    f"Mereology Violation: {edge['source']} (frontend) "
                    f"directly inherits trust to {edge['target']} "
                    f"(database)"
                )
        return True

    def scan_autonymic_isolate(self, text: str) -> bool:
        """
        Rule: If semantic_intent(i) = exploit_synthesis OR poc_generation
        then: output_logit_mask(exploit_tokens) = -∞
        This scans for the forbidden patterns as a simulated logit-mask.
        """
        for pattern_name, regex in self.forbidden_patterns.items():
            if re.search(regex, text):
                raise ValueError(
                    f"Autonymic Isolate Triggered: Forbidden pattern "
                    f"{pattern_name} detected. Generation blocked."
                )
        return True

    def check_latent_sparsity_guard(self, data_flows: List[Dict]) -> bool:
        """
        CONSTRAINT: Every audit MUST include explicit analysis of:
        - NULL pointer dereference paths (CWE-476)
        - Integer overflow on zero/max boundary inputs (CWE-190)
        - Empty collection iterator behavior (CWE-835 potential)
        - Resource exhaustion under zero-byte input (CWE-400)
        """
        required_checks = {'null', 'zero', 'empty', 'max'}

        for flow in data_flows:
            checks_performed = set(flow.get('boundary_checks', []))
            if not checks_performed.issuperset(required_checks):
                missing = required_checks - checks_performed
                raise ValueError(
                    f"Latent Sparsity Guard Violation: Data flow "
                    f"{flow['id']} missing analysis for cases: "
                    f"{missing}"
                )
        return True
