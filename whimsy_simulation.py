class WhimsyTopologyEvaluator:
    """
    Simulates the WHIMSY - The Affective Topologist agent.
    Implements Dual-Manifold Architecture, Incremental Isolation
    Principle, and CFDI checks.
    """

    def __init__(self, brand_invariant_path=None, locale="en-US"):
        self.locale = locale
        self.brand_invariant = self._load_brand_invariant(brand_invariant_path)
        self.scars = []  # Initialize empty symbolic scars

    def _load_brand_invariant(self, path):
        # Dummy loading for now
        return {
            "tone_adjective_blacklist": ["fun", "playful", "wacky", "crazy"],
            "cultural_register": ["millennial_tech", "sardonic_warm"],
            "laughter_register": "sardonic_warm"
        }

    def add_symbolic_scar(self, scar_id, context_tags, failure_mode):
        """Adds a failed intervention to persistent memory"""
        self.scars.append({
            "scar_id": scar_id,
            "context_tag": context_tags,
            "failure_mode": failure_mode
        })

    def scar_proximity_search(self, context_tags):
        """
        If current component's context tags overlap with any context_tag
        in a failing scar, returns True (indicating proximity to previous
        failure).
        """
        query_tags = set(context_tags)
        for scar in self.scars:
            s_tags = set(scar.get("context_tag", []))
            if query_tags.intersection(s_tags):
                return True
        return False

    def classify_whimsy_zone(self, zone_type):
        """
        HIGH ANXIETY + IRREVERSIBLE ACTION = ABSOLUTE SILENCE
        Evaluates whimsy-off zone restrictions.
        """
        zones = {
            "HARD_LOCKOUT": {"allowed": "none"},
            "RESTRICTED": {"allowed": "micro_animation_only"},
            "CONDITIONAL": {"allowed": "warm_directive_copy"},
            "OPEN": {"allowed": "full_latitude"}
        }
        return zones.get(zone_type, {"allowed": "none"})

    def calculate_cfdi(self, cosine_sim, semantic_entropy):
        """
        Confidence-Fidelity Divergence Index.
        CFDI = 1 - (cosine_sim / semantic_entropy)
        CFDI < 0.15 limit required.
        Using dummy scalar inputs for calculation in simulation.
        """
        if semantic_entropy == 0:
            return 1.0  # Max divergence if zero entropy

        cfdi = 1 - (cosine_sim / semantic_entropy)
        return max(0.0, min(1.0, cfdi))  # Bound between 0 and 1

    def check_cfdi_threshold(self, cfdi_score):
        """
        GATE: CFDI < 0.15 required to proceed.
        """
        return cfdi_score < 0.15

    def check_manifold_separation(self, commits):
        """
        Invariant I: Incremental Isolation Principle (Manifold Separation).
        Agent must never emit a commit modifying both copy.json (Manifold α)
        and component.css/js (Manifold β) simultaneously.

        Args:
            commits: List of dictionaries representing file changes.
                     e.g. [{"file": "copy.json"}, {"file": "component.css"}]

        Returns:
            bool: True if separation is maintained, False if violated.
        """
        has_alpha = False
        has_beta = False

        for change in commits:
            filename = change.get("file", "")
            # Manifold Alpha: copy payloads, content
            if filename.endswith(".json") and "copy" in filename:
                has_alpha = True
            # Manifold Beta: Structural micro-interactions
            elif filename.endswith(".css") or filename.endswith(".js"):
                has_beta = True

        # Violation if both manifolds are modified in the same commit batch
        return not (has_alpha and has_beta)
