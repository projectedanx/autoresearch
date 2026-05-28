

class VortexArchitectEvaluator:
    def __init__(self):
        pass

    def detect_betti_1_loop(self, execution_trace):
        """
        Detects a Betti-1 Loop by finding a cycle of (updating -> failing -> reverting).  # noqa: E501
        execution_trace is a list of string states.
        We look for the pattern: ['updating', 'failing', 'reverting'] occurring cyclically.  # noqa: E501
        """
        pattern = ['updating', 'failing', 'reverting']
        n = len(pattern)
        if len(execution_trace) < n * 2:
            return False

        # Check if the trace contains at least two consecutive occurrences of the pattern  # noqa: E501
        for i in range(len(execution_trace) - n * 2 + 1):
            if execution_trace[i:i+n] == pattern and execution_trace[i+n:i+n*2] == pattern:  # noqa: E501
                return True
        return False

    def check_semantic_mutex_locking(self, agent_processes):
        """
        Ensures no overlapping locked resources using set.isdisjoint().
        agent_processes is a dict mapping agent_id to a list (or set) of locked resources.  # noqa: E501
        """
        all_locked = set()
        for agent, resources in agent_processes.items():
            res_set = set(resources)
            if not all_locked.isdisjoint(res_set):
                return False
            all_locked.update(res_set)
        return True

    def evaluate_pal2v(self, conflict_a_weight, conflict_b_weight):
        """
        Applies Paraconsistent Annotated Logic (PAL2v) to resolve conflict.
        The dominant frame gets multiplied by the Golden Ratio (ϕ = 1.618),
        and the subordinate frame gets 1.000 multiplier.
        Returns the resolved weights as a tuple.
        """
        phi = 1.618
        if conflict_a_weight >= conflict_b_weight:
            return (conflict_a_weight * phi, conflict_b_weight * 1.0)
        else:
            return (conflict_a_weight * 1.0, conflict_b_weight * phi)
