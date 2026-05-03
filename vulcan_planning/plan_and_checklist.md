# Plan and Checklist for VULCAN Implementation

## Value of AI and Human Collaboration
- **Human Value**: Humans provide the abstract geometric topology boundary, NFR requirements, and subjective business logic constraints (e.g., team topologies, deployment cadences).
- **AI Value**: AI executes the Topological Causal Sculpting, rapidly identifying failure geometries (Symbolic Scars), computing the mathematical Betti-1 loops, evaluating CFDI, and mapping the exact boundary dimensions without cognitive bias or semantic saponification.
- **Inversion for Emergence**: Instead of the AI merely generating code based on human description, the AI acts as a rigid topological router and constraint engine (The Brutalist). It mathematically rejects invalid architectural topologies, forcing the human into a Plausibility Oracle Loop. This flips the dynamic: the AI establishes the physics and laws of the system, and the human provides the energy (intent).

## Execution Plan
1. **Understand Constraints**: Parse the VULCAN Frontmatter prompt to implement its required simulations and behaviors (AEW Nitinol Core, 10-Pattern Failure Taxonomy, Immune-Aware Petzold Sequence, Blast Radius Analysis).
2. **Generate Program Markdown**: Create `generate_program_vulcan.py` to programmatically assemble and write the exact VULCAN prompt text to `program_vulcan.md` to avoid output length limits and ensure strict formatting.
3. **Implement Simulation Evaluator**: Rewrite `vulcan_simulation.py` to include `VULCANTopologyEvaluator` class that functionally simulates:
   - `check_mereological_mandate`: Validates zero cross-domain state mutation calls (Rule 1).
   - `check_shared_database_anathema`: Detects and rejects shared database antipatterns (Rule 2).
   - `evaluate_nfr_gate`: Validates minimum viable architecture based on NFR constraints (Rule 3).
   - `check_cfdi_brake`: Measures CFDI divergence and triggers Epistemic Escrow on physical law violations (Rule 4).
   - `analyze_blast_radius`: Computes DAG in-degree to flag nodes with >20% blast radius.
4. **Write Unit Tests**: Add `tests/test_vulcan_simulation.py` and ensure >90% coverage for the new logic, using `unittest`.
5. **Update Repository Documentation**: Update `README.md` to reflect the new feature, documenting the synthesis of AI and Human value and lessons learned for VULCAN.
6. **Lint and Pre-commit**: Ensure 0 flake8 violations (`uvx flake8`) and that all tests pass before final commit.

## Implementation Checklist
- [ ] Create `vulcan_planning` directory and `plan_and_checklist.md`.
- [ ] Create `generate_program_vulcan.py`.
- [ ] Run `generate_program_vulcan.py` to update `program_vulcan.md`.
- [ ] Rewrite `vulcan_simulation.py` to match the 10 failure patterns, blast radius, NFR gate, and mereological rules.
- [ ] Implement `tests/test_vulcan_simulation.py`.
- [ ] Run `uv run python -m unittest discover tests` and verify tests pass.
- [ ] Run `uvx flake8` and fix any issues.
- [ ] Update `README.md` with features and lessons learned.
- [ ] Request Pre-Commit Instructions.
