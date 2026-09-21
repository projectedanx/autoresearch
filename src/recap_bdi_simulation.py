import re
from typing import List, Dict, Any, Optional

class ReCAPNode:
    """
    A node in the ReCAP dynamic context tree.
    """
    def __init__(self, desc: str, parent: Optional['ReCAPNode'] = None):
        self.desc = desc
        self.subtask_list: List[str] = []
        self.children_list: List['ReCAPNode'] = []
        self.obs_list: List[str] = []
        self.think_list: List[str] = []
        self.parent = parent
        self.status = "PENDING" # PENDING, ACTIVE, COMPLETED, FAILED

    def add_subtask(self, task: str):
        self.subtask_list.append(task)

    def add_child(self, child_node: 'ReCAPNode'):
        self.children_list.append(child_node)

    def add_observation(self, obs: str):
        self.obs_list.append(obs)


class BDISolver:
    """
    Simulates the Control Module (System 2 - BDI Solver/Filter).
    """
    def parse_bdi(self, text: str) -> Dict[str, str]:
        """
        Parses #Beliefs, #Desires, #Intentions.
        """
        beliefs = ""
        desires = ""
        intentions = ""

        b_match = re.search(r'#Beliefs\s*:\s*(.*?)(?=#Desires|#Intentions|$)', text, re.IGNORECASE | re.DOTALL)
        d_match = re.search(r'#Desires\s*:\s*(.*?)(?=#Beliefs|#Intentions|$)', text, re.IGNORECASE | re.DOTALL)
        i_match = re.search(r'#Intentions\s*:\s*(.*?)(?=#Beliefs|#Desires|$)', text, re.IGNORECASE | re.DOTALL)

        if b_match: beliefs = b_match.group(1).strip()
        if d_match: desires = d_match.group(1).strip()
        if i_match: intentions = i_match.group(1).strip()

        return {
            "beliefs": beliefs,
            "desires": desires,
            "intentions": intentions
        }

    def verify_action(self, bdi_state: Dict[str, str], env_state: Dict[str, Any]) -> bool:
        """
        Symbolic Verification Loop.
        Checks for Sussman Anomaly: e.g. intending to use a station that is blocked.
        """
        beliefs = bdi_state.get("beliefs", "").lower()
        intentions = bdi_state.get("intentions", "").lower()

        # Sussman Anomaly check
        if "use station" in intentions or "assemble" in intentions:
            if "station is blocked" in beliefs or env_state.get("station_blocked", False):
                # Logical inconsistency: Trying to use a blocked station
                return False

        return True


class ReCAPBDIEvaluator:
    """
    Manages the Dynamic Context Tree and BDI integration.
    """
    def __init__(self):
        self.root: Optional[ReCAPNode] = None
        self.active_node: Optional[ReCAPNode] = None
        self.solver = BDISolver()
        self.env_state = {"station_blocked": False}

    def set_env_state(self, key: str, value: Any):
        self.env_state[key] = value

    def initialize_tree(self, goal: str):
        self.root = ReCAPNode(goal)
        self.active_node = self.root

    def downward_decomposition(self, subtasks: List[str]):
        """
        Plan-Ahead: Decomposes a goal into an ordered list of subtasks.
        """
        if not self.active_node:
            return

        for task in subtasks:
            self.active_node.add_subtask(task)

        # Execute head item
        if self.active_node.subtask_list:
            head_task = self.active_node.subtask_list[0]
            child = ReCAPNode(head_task, parent=self.active_node)
            self.active_node.add_child(child)
            self.active_node = child

    def execute_intention(self, bdi_text: str) -> str:
        """
        Parses BDI, verifies, and executes. Triggers upward backtracking on failure.
        """
        if not self.active_node:
            return "NO_ACTIVE_NODE"

        bdi_state = self.solver.parse_bdi(bdi_text)
        is_valid = self.solver.verify_action(bdi_state, self.env_state)

        if is_valid:
            self.active_node.status = "COMPLETED"
            self.active_node.add_observation("Action succeeded.")
            # Move back to parent to continue subtasks
            if self.active_node.parent:
                parent = self.active_node.parent
                if parent.subtask_list:
                    parent.subtask_list.pop(0) # Remove completed subtask
                self.active_node = parent
            return "SUCCESS"
        else:
            self.active_node.status = "FAILED"
            self.active_node.add_observation("Action failed: Sussman Anomaly or Safety Violation.")
            return self.upward_backtracking()

    def upward_backtracking(self) -> str:
        """
        Structured Injection: When child fails, parent plan is re-injected,
        and we backtrack.
        """
        if not self.active_node or not self.active_node.parent:
            return "FAILURE_ROOT"

        parent = self.active_node.parent
        # Parent intercepts failure, prunes invalid subtree (the failed child)
        if self.active_node in parent.children_list:
            # We keep it for record, but we could prune it.
            # In ReCAP, we re-inject the strategic goal and trigger an alternative branch.
            pass

        parent.add_observation(f"Child task '{self.active_node.desc}' failed. Replanning.")

        # Pop the failed subtask from parent's list
        if parent.subtask_list and parent.subtask_list[0] == self.active_node.desc:
            parent.subtask_list.pop(0)

        self.active_node = parent
        return "BACKTRACKED"
