import unittest
import math


class ALETHEONTopologyEvaluator:
    def __init__(self):
        self.ssa_scars = []  # Symbolic Scar Archive
        self.ecosystem_manifolds = {
            "Rust": set(),
            "Python": set()
        }

    def add_scar(self, scar_id: str, signature: dict):
        self.ssa_scars.append({
            "scar_id": scar_id,
            "signature": signature
        })

    def check_scar_isomorphism(self, current_signature: dict,
                               threshold: float = 0.78) -> bool:
        """
        Rule 4: The Symbolic Scar Inheritance Rule
        Calculates a simplified cosine similarity between tool signatures.
        """
        for scar in self.ssa_scars:
            scar_sig = scar["signature"]

            # Simple intersection / union for simulation of cosine similarity
            # over binary features
            common_keys = set(current_signature.keys()
                              ).intersection(set(scar_sig.keys()))
            if not common_keys:
                continue

            dot_product = sum(
                current_signature[k] * scar_sig[k] for k in common_keys)
            norm_a = math.sqrt(sum(v**2 for v in current_signature.values()))
            norm_b = math.sqrt(sum(v**2 for v in scar_sig.values()))

            if norm_a == 0 or norm_b == 0:
                continue

            similarity = dot_product / (norm_a * norm_b)
            if similarity > threshold:
                return True
        return False

    def add_to_ecosystem(self, tool_name: str, ecosystem: str):
        if ecosystem in self.ecosystem_manifolds:
            self.ecosystem_manifolds[ecosystem].add(tool_name)

    def check_epistemic_isolation(self, tool_a: str, tool_b: str) -> bool:
        """
        Rule 2: The Epistemic Isolation Rule (The Pluriversal Invariant).
        Cross-ecosystem comparison is permitted only if explicitly validated,
        otherwise it's an Ontological Shear. Here, for simulation, we
        reject direct comparison if tools belong to different known
        ecosystems.
        """
        a_ecosystem = None
        b_ecosystem = None

        for eco, tools in self.ecosystem_manifolds.items():
            if tool_a in tools:
                a_ecosystem = eco
            if tool_b in tools:
                b_ecosystem = eco

        if a_ecosystem and b_ecosystem and a_ecosystem != b_ecosystem:
            return False
        return True

    def check_epistemic_quarantine(self, cfdi: float,
                                   threshold: float = 0.15) -> bool:
        """
        Rule 1: The Epistemic Quarantine Rule.
        CFDI threshold: 0.15. If divergence exceeds this, +++EpistemicEscrow
        `halt_on_divergence=true` suspends the evaluation stream.
        """
        return cfdi <= threshold

    def calculate_betti_1(self, documentation_claims: list,
                          codebase_realities: list) -> int:
        """
        Phase 3: The Betti-1 Integration Test
        Each irreconcilable mismatch constitutes a Betti-1 loop.
        """
        # Simplified: each claim without a matching reality creates a hole.
        # In this simulation, we'll just return the absolute difference
        # in count or if they are dicts, we could do exact matching.
        # Let's do simple count diff for now.
        return max(0, len(documentation_claims) - len(codebase_realities))


class TestALETHEONRules(unittest.TestCase):
    def test_epistemic_quarantine_pass(self):
        evaluator = ALETHEONTopologyEvaluator()
        self.assertTrue(evaluator.check_epistemic_quarantine(0.10))

    def test_epistemic_quarantine_fail(self):
        evaluator = ALETHEONTopologyEvaluator()
        self.assertFalse(evaluator.check_epistemic_quarantine(0.25))

    def test_epistemic_isolation_pass(self):
        evaluator = ALETHEONTopologyEvaluator()
        evaluator.add_to_ecosystem("tool_a", "Python")
        evaluator.add_to_ecosystem("tool_b", "Python")
        self.assertTrue(
            evaluator.check_epistemic_isolation("tool_a", "tool_b"))

    def test_epistemic_isolation_fail(self):
        evaluator = ALETHEONTopologyEvaluator()
        evaluator.add_to_ecosystem("tool_a", "Python")
        evaluator.add_to_ecosystem("tool_b", "Rust")
        self.assertFalse(
            evaluator.check_epistemic_isolation("tool_a", "tool_b"))

    def test_scar_isomorphism_pass(self):
        evaluator = ALETHEONTopologyEvaluator()
        scar_sig = {"api_latency": 1, "memory_leak": 1, "bad_docs": 1}
        evaluator.add_scar("SCAR-001", scar_sig)

        current_sig = {"api_latency": 1, "memory_leak": 1, "bad_docs": 1}
        self.assertTrue(evaluator.check_scar_isomorphism(current_sig))

    def test_scar_isomorphism_fail(self):
        evaluator = ALETHEONTopologyEvaluator()
        scar_sig = {"api_latency": 1, "memory_leak": 1, "bad_docs": 1}
        evaluator.add_scar("SCAR-001", scar_sig)

        current_sig = {"good_docs": 1, "low_latency": 1}
        self.assertFalse(evaluator.check_scar_isomorphism(current_sig))

    def test_betti_1_calculation(self):
        evaluator = ALETHEONTopologyEvaluator()
        claims = ["fast", "secure", "easy"]
        realities = ["fast", "secure"]  # "easy" is missing in reality
        betti_1 = evaluator.calculate_betti_1(claims, realities)
        self.assertEqual(betti_1, 1)


if __name__ == '__main__':
    unittest.main()
