# ReCAP-BDI Epistemic Cognitive Harness Specification

## Abstract
In artificial social intelligence, the **thought-action gap** represents a critical systems-engineering failure where a model’s high-fidelity internal representations decouple from its actual behavioral execution or strategic policy. This gap is structurally illuminated by the divergence between **Literal Theory of Mind (ToM)** and **Functional Theory of Mind (ToM)**. This specification details the ReCAP-BDI (Recursive Context-Aware Planning with Belief-Desire-Intention) framework to bridge this gap.

## 1. Automated Discovery and Constraint Mining

*   **Invariant 1 (The Deliberation Penalty):** Forcing an autoregressive model to execute a flat, sequential Chain-of-Thought (CoT) scaffold in high-context social or conversational dynamics acts as a severe cognitive constraint.
*   **Invariant 2 (The Predict-Then-Optimize Bottleneck):** Standard sequential prompting (e.g., ReAct) separates prediction from action optimization. When task horizons extend, early plans and observations drift out of the model's active attention and KV cache, causing the agent to lose its strategic intent and lapse into redundant, infinite failure loops.
*   **Soft Target (Epistemic Optimization):** Maximize expected utility and minimize step-wise regret under dynamic, closed-loop environmental feedback.

## 2. Isomorphic Formalization

### A. The Belief-Desire-Intention (BDI) State Transition Matrix
The agent’s internal state space is formalized around the triadic BDI framework:
- **Beliefs:** World knowledge.
- **Desires:** High-level goals.
- **Intentions:** Concrete plans of action.

### B. The Dynamic Context Tree (ReCAP)
For long-horizon tasks, we replace flat linear contexts with a dynamic context tree. A task node is formalized as a structured tuple: `<desc, subtask_list, children_list, obs_list, think_list>`. This tree manages recursive execution via downward decomposition and upward backtracking.

## 3. Parametric Trade-off Modeling

*   **Context Window vs. KV Cache Overhead:** Bounding the active prompt size to a constant scale.
*   **Divergence Functions in Distillation:** Mechanistic Circuit Distillation for transferring ToM capabilities.
*   **The Decoupled vs. Embodied ToM Trade-off:** Grounding beliefs in environmental actions.

## 4. Continuous Falsification and Edge-Case Stress Testing

*   **The Rock, Paper, Scissors "Nash Trap"**
*   **The Sussman/Burger Anomaly (Blocked Station Deadlock)**

## Finalized Response Output: The Inferred Harness Specification

This harness operationalizes the PEACE Meta-Architecture:
1.  **Retrieval Module:** Extracts task-relevant contextual priors.
2.  **Cognition Module (System 1):** Generates fast, associative hypotheses.
3.  **Control Module (System 2):** Serves as a meta-cognitive overseer. Parsed into formal BDI logic, evaluated against constraints.
4.  **Action Module:** Executes authorized primitive commands.
5.  **Memory Module:** Dynamically manages state tracking using a sliding window and a context tree.
