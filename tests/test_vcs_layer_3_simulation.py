import pytest
from src.vcs_layer_3_simulation import VCSLayer3Evaluator, CodeState, SICSchema

def test_successful_verification_attestation():
    initial_state = CodeState(commit_hash="init123", content="print('hello')", is_stable=True)
    evaluator = VCSLayer3Evaluator(initial_state)

    sic1 = SICSchema(
        constraint_id="SIC_VERIFY",
        assertion_type="ASSERT",
        description="ASSERT strict type safety",
        verification_target="npm run lint",
        required_metric_threshold=0.85,
        failsafe_command="git checkout"
    )
    evaluator.add_sic(sic1)

    new_state = CodeState(commit_hash="mut456", content="print('hello world')", anomalies=[])

    result = evaluator.execute_closed_loop(new_state, "SIC_VERIFY")
    assert result == "COMMITTED"
    assert evaluator.state.is_stable is True
    assert evaluator.error_budget == 3
    assert evaluator.epistemic_escrow is False

def test_verification_failure_f_ipi_loop():
    initial_state = CodeState(commit_hash="init123", content="initial", is_stable=True)
    evaluator = VCSLayer3Evaluator(initial_state)

    sic1 = SICSchema(
        constraint_id="SIC_ARCH",
        assertion_type="FORBID",
        description="FORBID unauthorized external connections",
        verification_target="/security:analyze",
        required_metric_threshold=1.0,
        failsafe_command="git checkout"
    )
    evaluator.add_sic(sic1)

    # Introduce an anomaly that will trigger the failure path
    new_state = CodeState(commit_hash="mut456", content="import request", anomalies=["Violation of SIC_ARCH"])

    result = evaluator.execute_closed_loop(new_state, "SIC_ARCH")
    assert result == "F_IPI_RETRY"
    assert evaluator.error_budget == 2
    assert len(evaluator.scar_tissue_archive) == 1
    assert "ep_error: Violation of SIC_ARCH" in evaluator.active_gemini_context

def test_epistemic_escrow_circuit_breaker():
    initial_state = CodeState(commit_hash="init123", content="initial", is_stable=True)
    evaluator = VCSLayer3Evaluator(initial_state)

    sic1 = SICSchema(
        constraint_id="SIC_VERIFY",
        assertion_type="ASSERT",
        description="ASSERT strict type safety",
        verification_target="npm run lint",
        required_metric_threshold=0.85,
        failsafe_command="git checkout"
    )
    evaluator.add_sic(sic1)

    # Exhaust the error budget
    new_state = CodeState(commit_hash="mut_bad", content="bad code", anomalies=["Violation of SIC_VERIFY"])

    res1 = evaluator.execute_closed_loop(new_state, "SIC_VERIFY")
    assert res1 == "F_IPI_RETRY"
    assert evaluator.error_budget == 2

    res2 = evaluator.execute_closed_loop(new_state, "SIC_VERIFY")
    assert res2 == "F_IPI_RETRY"
    assert evaluator.error_budget == 1

    res3 = evaluator.execute_closed_loop(new_state, "SIC_VERIFY")
    assert res3 == "HALTED_EPISTEMIC_ESCROW"
    assert evaluator.error_budget == 0
    assert evaluator.epistemic_escrow is True
    assert evaluator.state.content == "ROLLBACK_TO_INITIAL"

    # Attempting to mutate in Escrow should raise RuntimeError
    res4 = evaluator.execute_closed_loop(new_state, "SIC_VERIFY")
    assert "Cannot mutate code while in Epistemic Escrow." in res4

def test_parametric_tradeoff_feasibility_frontier():
    evaluator = VCSLayer3Evaluator(CodeState("init", "code"))
    assert evaluator.evaluate_feasibility_frontier("LOW") == "LIGHTWEIGHT_SYNTAX_LINT"
    assert evaluator.evaluate_feasibility_frontier("HIGH") == "FULL_REGRESSION_AND_HITL"
    assert evaluator.evaluate_feasibility_frontier("MED") == "STANDARD_VERIFICATION"

def test_mutation_testing_falsification():
    initial_state = CodeState(commit_hash="init", content="code", is_stable=True)
    evaluator = VCSLayer3Evaluator(initial_state)

    evaluator.inject_mutation_anomaly("ANOMALY_SIC_VERIFY_BYPASS")
    assert "ANOMALY_SIC_VERIFY_BYPASS" in evaluator.state.anomalies
