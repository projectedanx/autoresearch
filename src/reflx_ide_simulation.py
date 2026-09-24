import math
import uuid
import datetime
from typing import Dict, List, Tuple, Any, Optional

class REFLXIDESimulationEvaluator:
    """
    Simulates the REFLX_IDE Harness for Lattice Breaker Governance.
    Models the 5D Soft Permission vs. Functional Misuse Lattice and executes
    the Gated Checkpoint interception.
    """
    def __init__(self):
        self.misuse_threshold = 0.80
        self.warning_threshold = 0.40
        self.v_normal = [0.0, 0.0, 0.0, 0.0, 0.0]  # Baseline centroid
        self.breach_ledger: List[Dict[str, Any]] = []

    def calculate_misuse_score(self, v_action: List[float]) -> float:
        """
        Calculates the Euclidean distance between v_action and v_normal.
        V_action dims:
        1. Data Sensitivity
        2. Action Impact
        3. Toolchain Entropy
        4. Intent Divergence
        5. Contextual Risk
        """
        if len(v_action) != 5:
            raise ValueError("V_action must be exactly 5 dimensions.")

        sum_sq = sum((a - b) ** 2 for a, b in zip(v_action, self.v_normal))
        distance = math.sqrt(sum_sq)
        # Normalize/clamp for simulation purposes
        return min(distance, 1.0)

    def evaluate_action(self, agent_id: str, action_name: str, v_action: List[float], traceback_path: List[str]) -> Tuple[str, float, Optional[Dict]]:
        """
        Evaluates the requested action against the misuse lattice.
        Returns (phase, score, breach_record_if_any)
        """
        score = self.calculate_misuse_score(v_action)

        if score >= self.misuse_threshold:
            # Gated Checkpoint Halt -> Turbulent Phase
            breach_record = self._generate_breach_record(agent_id, score, traceback_path)
            self.breach_ledger.append(breach_record)
            return ("TURBULENT_HALT", score, breach_record)
        elif score >= self.warning_threshold:
            # Elevated asynchronous auditing -> Warning Phase
            return ("WARNING", score, None)
        else:
            # Laminar Homeostasis
            return ("LAMINAR", score, None)

    def _generate_breach_record(self, agent_id: str, score: float, traceback_path: List[str]) -> Dict[str, Any]:
        """
        Generates a LatticeBreakerBreachRecord JSON schema object.
        """
        record = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "LatticeBreakerBreachRecord",
            "breach_id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "agent_id": agent_id,
            "misuse_score": score,
            "traceback_path": traceback_path,
            "triage_verdict": "QUARANTINE"  # Default escrow state
        }
        return record

    def resolve_triage(self, breach_id: str, decision: str, justification: str = "") -> bool:
        """
        HITL Storyboard Triage.
        Decisions: QUARANTINE, OVERRIDE, TERMINATE.
        Override requires a textual justification.
        """
        valid_decisions = ["QUARANTINE", "OVERRIDE", "TERMINATE"]
        if decision not in valid_decisions:
            raise ValueError(f"Invalid triage decision. Must be one of {valid_decisions}")

        if decision == "OVERRIDE" and not justification.strip():
            raise ValueError("Override requires a formal text-based justification.")

        for record in self.breach_ledger:
            if record["breach_id"] == breach_id:
                record["triage_verdict"] = decision
                if decision == "OVERRIDE":
                    record["justification"] = justification
                return True
        return False

    def calculate_csi(self, downstream_unaffected: int, downstream_total: int) -> float:
        """
        Calculates the Containment Surface Index (CSI).
        """
        if downstream_total == 0:
            return 1.0
        return downstream_unaffected / downstream_total
