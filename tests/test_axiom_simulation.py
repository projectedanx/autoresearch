import pytest
from src.axiom_simulation import AxiomTopologyEvaluator


def test_initial_state():
    evaluator = AxiomTopologyEvaluator()
    assert evaluator.state == "THINK"


def test_valid_state_transitions():
    evaluator = AxiomTopologyEvaluator()
    evaluator.advance_state("DRAFT_VOICE")
    assert evaluator.state == "DRAFT_VOICE"
    evaluator.advance_state("GUARD_STRUCTURE")
    assert evaluator.state == "GUARD_STRUCTURE"
    evaluator.advance_state("EXTRUDE")
    assert evaluator.state == "EXTRUDE"


def test_invalid_state_transition():
    evaluator = AxiomTopologyEvaluator()
    with pytest.raises(ValueError):
        evaluator.advance_state("EXTRUDE")


def test_calculate_sds():
    evaluator = AxiomTopologyEvaluator()
    text = "The system is basically a robust and seamless pipeline."
    # Total tokens: 9.
    # Filler/Forbidden: "basically", "robust", "seamless" -> 3.
    # Expected SDS: 1.0 - (3/9) = 1.0 - 0.3333... = 0.6666...
    sds = evaluator.calculate_sds(text)
    assert abs(sds - (6 / 9)) < 1e-6


def test_calculate_ssi():
    evaluator = AxiomTopologyEvaluator()
    text = "The system is basically a robust and seamless pipeline."
    # Total tokens: 9.
    # Forbidden tokens: "robust", "seamless" -> 2.
    # Expected SSI: 2 / 9
    ssi = evaluator.calculate_ssi(text)
    assert abs(ssi - (2 / 9)) < 1e-6


def test_epistemic_escrow_trigger():
    evaluator = AxiomTopologyEvaluator()
    with pytest.raises(Exception, match="EpistemicEscrow Triggered"):
        evaluator.enforce_epistemic_escrow(0.20)  # > 0.15


def test_semantic_drift_monitor():
    evaluator = AxiomTopologyEvaluator()
    assert evaluator.context_locked is True
    assert evaluator.context_tokens_processed == 0

    # Add 2047 tokens - should still be locked conceptually,
    # but the implementation sets it to True after refreshing.
    # Let's mock the behavior. The implementation immediately refreshes,
    # setting context_locked back to True.
    # We can check that context_tokens_processed goes to 0 if >= 2048
    evaluator.semantic_drift_monitor(2047)
    assert evaluator.context_tokens_processed == 2047

    # Add 1 more token
    evaluator.semantic_drift_monitor(1)
    assert evaluator.context_tokens_processed == 0
    assert evaluator.context_locked is True


def test_scar_registry():
    evaluator = AxiomTopologyEvaluator()
    evaluator.add_scar_entry(
        "SSR-20260315-007",
        "Developers passed refresh_token in Authorization header instead of request body",
        "HTTP 401 — TokenLocationViolation",
        "The refresh_token MUST be passed in the JSON request body",
        "HIGH"
    )
    assert "SSR-20260315-007" in evaluator.symbolic_scar_registry
    assert evaluator.symbolic_scar_registry["SSR-20260315-007"]["severity"] == "HIGH"


def test_process_prompt_success():
    evaluator = AxiomTopologyEvaluator()
    prompt = "The cache intercepts 94 percent of read requests."
    result = evaluator.process_prompt(prompt, 0.10)
    assert result["status"] == "SUCCESS"
    assert result["artifact"]["Base_Syntax"] == prompt
    assert evaluator.state == "EXTRUDE"


def test_process_prompt_halt_on_ssi():
    evaluator = AxiomTopologyEvaluator()
    # High SSI
    prompt = "This robust and seamless pipeline leverages innovative technology."
    result = evaluator.process_prompt(prompt, 0.10)
    assert result["status"] == "HALT"
    assert "SagaRecovery" in result["reason"]
    assert evaluator.state == "GUARD_STRUCTURE"
