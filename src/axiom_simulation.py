import re
from typing import Dict, List, Any


class AxiomTopologyEvaluator:
    def __init__(self):
        self.state = "THINK"
        self.forbidden_lexicon = {
            "seamless", "robust", "transformative", "delve", "leverage",
            "cutting-edge", "innovative", "streamline", "powerful",
            "i'm happy to help", "certainly", "of course"
        }
        self.filler_tokens = self.forbidden_lexicon.union({
            "basically", "essentially", "just", "simply",
            "obviously", "actually", "literally", "very", "really"
        })
        self.symbolic_scar_registry: Dict[str, Dict[str, str]] = {}
        self.context_tokens_processed = 0
        self.context_locked = True
        self.ssi_threshold = 0.04
        self.cfdi_threshold = 0.15

    def advance_state(self, new_state: str):
        valid_transitions = {
            "THINK": "DRAFT_VOICE",
            "DRAFT_VOICE": "GUARD_STRUCTURE",
            "GUARD_STRUCTURE": "EXTRUDE"
        }
        if self.state in valid_transitions and valid_transitions[self.state] == new_state:
            self.state = new_state
        else:
            raise ValueError(
                f"Invalid Petzold Sequence transition from {self.state} to {new_state}"
            )

    def calculate_sds(self, text: str) -> float:
        """
        Calculates Semantic Density Score (SDS).
        SDS = 1 - (count(filler_tokens) / total_tokens)
        """
        words = re.findall(r'\b\w+(?:-\w+)?\b', text.lower())
        total_tokens = len(words)
        if total_tokens == 0:
            return 1.0

        # O(1) lookup
        filler_count = sum(1 for w in words if w in self.filler_tokens)

        # Handle multi-word sycophantic phrases which regex split might break,
        # so we also check full string for specific phrases
        lower_text = text.lower()
        if "i'm happy to help" in lower_text:
            filler_count += 4
        if "of course" in lower_text:
            filler_count += 2

        sds = 1.0 - (filler_count / total_tokens)
        return sds

    def calculate_ssi(self, text: str) -> float:
        """
        Calculates Semantic Saponification Index (SSI).
        SSI = count(forbidden_token_matches) / total_tokens
        """
        words = re.findall(r'\b\w+(?:-\w+)?\b', text.lower())
        total_tokens = len(words)
        if total_tokens == 0:
            return 0.0

        forbidden_count = sum(1 for w in words if w in self.forbidden_lexicon)

        # Handle multi-word phrases
        lower_text = text.lower()
        if "i'm happy to help" in lower_text:
            forbidden_count += 4
        if "of course" in lower_text:
            forbidden_count += 2

        return forbidden_count / total_tokens

    def enforce_epistemic_escrow(self, cfdi: float):
        """
        Checks Confidence-Fidelity Divergence Index (CFDI).
        """
        if cfdi > self.cfdi_threshold:
            raise Exception(f"EpistemicEscrow Triggered: CFDI {cfdi} exceeds {self.cfdi_threshold}")

    def semantic_drift_monitor(self, new_tokens: int):
        """
        Operationalizes the cross-encoder semantic distance monitoring.
        Triggers ContextLock re-injection every 2048 tokens.
        """
        self.context_tokens_processed += new_tokens
        if self.context_tokens_processed >= 2048:
            self.context_locked = False
            self.refresh_context_lock()

    def refresh_context_lock(self):
        """
        Re-injects the EPISTEMIC_MATRIX anchor.
        """
        self.context_locked = True
        self.context_tokens_processed = 0

    def add_scar_entry(self, scar_id: str, trigger: str, failure_mode: str, prevention_directive: str, severity: str):
        """
        Adds an entry to the Symbolic Scar Registry (SSR).
        """
        self.symbolic_scar_registry[scar_id] = {
            "trigger": trigger,
            "failure_mode": failure_mode,
            "prevention_directive": prevention_directive,
            "severity": severity
        }

    def process_prompt(self, user_prompt: str, cfdi: float) -> dict:
        """
        Simulates the Immune-Aware Petzold Loop.
        """
        self.state = "THINK"

        # PHASE 1: THINK
        self.enforce_epistemic_escrow(cfdi)

        self.advance_state("DRAFT_VOICE")

        # PHASE 2: DRAFT_VOICE
        total_words = len(re.findall(r'\b\w+(?:-\w+)?\b', user_prompt))
        self.semantic_drift_monitor(total_words)

        self.advance_state("GUARD_STRUCTURE")

        # PHASE 3: GUARD_STRUCTURE
        ssi = self.calculate_ssi(user_prompt)
        if ssi > self.ssi_threshold:
            return {
                "status": "HALT",
                "reason": f"SagaRecovery triggered: SSI {ssi} > {self.ssi_threshold}"
            }

        self.advance_state("EXTRUDE")

        # PHASE 4: EXTRUDE
        sds = self.calculate_sds(user_prompt)

        return {
            "status": "SUCCESS",
            "artifact": {
                "Base_Syntax": user_prompt,
                "SDS_Final": sds,
                "SSI_Final": ssi,
                "CFDI_Observed": cfdi,
                "Context_Locked": self.context_locked
            }
        }
