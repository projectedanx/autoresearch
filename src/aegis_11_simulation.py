import math
from typing import Dict, Any, List


class AEGIS11Evaluator:
    def __init__(self):
        self.state_tracking = {}

    def parse_hickam_topology(self, data: Dict[str, Any]) -> bool:
        """
        Validates the pre-generation scaffold (Hickam_Topology schema).
        Requires exact keys.
        """
        required_keys = {
            "Hickam_Orientation", "Contrastive_Delta",
            "Martensite_Metrics", "Consilience_Status"
        }
        if set(data.keys()) != required_keys:
            return False
        return True

    def calculate_cfdi(self, structural_coherence: float,
                       semantic_noise: float) -> float:
        """
        Calculates the Confidence-Fidelity Divergence Index (CFDI).
        Target: CFDI <= 0.12
        """
        if structural_coherence == 0:
            return 1.0  # Max divergence
        return semantic_noise / structural_coherence

    def apply_golden_ratio_synthesis(self, dominant_val: float,
                                     subordinate_val: float) -> float:
        """
        Synthesize two conflicting frameworks using the Golden Ratio protocol.
        Weights: 1.618 (dominant) and 1.000 (subordinate).
        Do not average. We represent them in structural tension
        by retaining their weighted sum.
        """
        phi = 1.618
        return (dominant_val * phi) + (subordinate_val * 1.000)

    def calculate_cosine_similarity(self, vec_a: List[float],
                                    vec_b: List[float]) -> float:
        """Calculates cosine similarity between two vectors."""
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            raise ValueError(
                "Vectors must be non-empty and of the same length.")
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def evaluate_exit_gate(self, constraints_satisfied: int,
                           total_constraints: int, target_vec: List[float],
                           generated_vec: List[float]) -> bool:
        """
        Computes the exit gate logic.
        IAR = constraints_satisfied / total_constraints
        SDS = 1 - CosineSimilarity(target_vec, generated_vec)
        Passes if IAR >= 0.98 AND SDS <= 0.05
        """
        if total_constraints <= 0:
            raise ValueError("Total constraints must be > 0")

        iar = constraints_satisfied / total_constraints
        sds = 1.0 - self.calculate_cosine_similarity(target_vec, generated_vec)

        return iar >= 0.98 and sds <= 0.05

    def check_cfdi_limit(self, cfdi: float) -> bool:
        """Check if CFDI is safely beneath maximum threshold of 0.1200."""
        return cfdi <= 0.12

    def extract_separable_grid(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        The Semantic Sandbox: Construct a SeparableGridParse
        to multidimensionally isolate variables, state mutations,
        and side effects.
        """
        isolated_grid = {
            "variables": set(),
            "state_mutations": [],
            "side_effects": []
        }
        for k, v in inputs.items():
            if k.startswith("var_"):
                isolated_grid["variables"].add(k)
            elif k.startswith("mut_"):
                isolated_grid["state_mutations"].append((k, v))
            elif k.startswith("eff_"):
                isolated_grid["side_effects"].append((k, v))
        return isolated_grid
