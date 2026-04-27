import math


class PDLLexiconEvaluator:
    """
    Simulates patterns and hypotheses defined in DRP-LEXICON-992.
    """

    def __init__(self):
        pass

    def calculate_saponification_weight(
            self, w0: float, lambda_rate: float, frequency: int) -> float:
        """
        PAT-007: Lexical Saponification Paradox
        W(t) = W₀·e^(−λ·f)
        """
        return w0 * math.exp(-lambda_rate * frequency)

    def check_saponification_onset(
            self, w0: float, current_weight: float) -> bool:
        """
        Saponification onset occurs when entity density drops by ~20%.
        """
        if w0 == 0:
            return False
        drop_percentage = (w0 - current_weight) / w0
        return drop_percentage >= 0.20

    def simulate_workflow_narrowing(
            self, initial_density: float, node_depth: int,
            has_context_lock: bool) -> float:
        """
        PAT-003: Workflow Narrowing Effect
        N>3 nodes without ContextLock = degradation onset.
        N>5 = catastrophic collapse (>40% drop).
        Returns simulated L2 Norm entity density.
        """
        if has_context_lock:
            # ContextLock prevents degradation
            return initial_density

        density = initial_density
        if node_depth > 5:
            # Catastrophic collapse (>40% drop) - simulating a 55% drop
            density = initial_density * 0.45
        elif node_depth > 3:
            # Degradation onset - simulating a 20% drop
            density = initial_density * 0.80

        return density

    def check_workflow_narrowing_collapse(
            self, initial_density: float, current_density: float) -> bool:
        """
        Returns True if L2 Norm entity density collapsed by >40%.
        """
        if initial_density == 0:
            return False
        drop = (initial_density - current_density) / initial_density
        return drop > 0.40

    def check_polyglot_hallucination_resonance(
            self, phronesis_index: float, cfdi: float) -> bool:
        """
        PAT-005: Polyglot Hallucination Resonance (PHR)
        Phronesis Index Φ < 0.05 = spectral gap collapse = PHR confirmed.
        OR CFDI > 0.15.
        """
        if phronesis_index < 0.05:
            return True
        if cfdi > 0.15:
            return True
        return False
