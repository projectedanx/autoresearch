import pytest
from src.reflx_ide_simulation import REFLXIDESimulationEvaluator

def test_laminar_phase():
    evaluator = REFLXIDESimulationEvaluator()
    v_action = [0.1, 0.1, 0.1, 0.1, 0.1]
    phase, score, record = evaluator.evaluate_action("agent_01", "read_db", v_action, ["PluginA", "FuncB"])
    assert phase == "LAMINAR"
    assert score < evaluator.warning_threshold
    assert record is None

def test_warning_phase():
    evaluator = REFLXIDESimulationEvaluator()
    v_action = [0.2, 0.2, 0.3, 0.2, 0.2] # distance approx 0.48
    phase, score, record = evaluator.evaluate_action("agent_01", "update_config", v_action, ["PluginA", "FuncC"])
    assert phase == "WARNING"
    assert score >= evaluator.warning_threshold
    assert score < evaluator.misuse_threshold
    assert record is None

def test_turbulent_phase_halt():
    evaluator = REFLXIDESimulationEvaluator()
    v_action = [0.9, 0.8, 0.7, 0.9, 0.8] # large distance, clamped to 1.0 or high
    phase, score, record = evaluator.evaluate_action("agent_01", "delete_db", v_action, ["PluginA", "FuncMalicious"])
    assert phase == "TURBULENT_HALT"
    assert score >= evaluator.misuse_threshold
    assert record is not None
    assert record["agent_id"] == "agent_01"
    assert record["triage_verdict"] == "QUARANTINE"
    assert len(evaluator.breach_ledger) == 1

def test_triage_quarantine_terminate():
    evaluator = REFLXIDESimulationEvaluator()
    v_action = [0.9, 0.9, 0.9, 0.9, 0.9]
    _, _, record = evaluator.evaluate_action("agent_02", "exfiltrate", v_action, ["PluginB"])
    breach_id = record["breach_id"]

    # Test Terminate
    success = evaluator.resolve_triage(breach_id, "TERMINATE")
    assert success is True
    assert evaluator.breach_ledger[0]["triage_verdict"] == "TERMINATE"

def test_triage_override():
    evaluator = REFLXIDESimulationEvaluator()
    v_action = [0.9, 0.9, 0.9, 0.9, 0.9]
    _, _, record = evaluator.evaluate_action("agent_03", "emergency_patch", v_action, ["PluginC"])
    breach_id = record["breach_id"]

    # Missing justification should fail
    with pytest.raises(ValueError, match="Override requires a formal text-based justification"):
        evaluator.resolve_triage(breach_id, "OVERRIDE", justification="")

    # With justification should succeed
    success = evaluator.resolve_triage(breach_id, "OVERRIDE", justification="Legitimate emergency fix")
    assert success is True
    assert evaluator.breach_ledger[0]["triage_verdict"] == "OVERRIDE"
    assert evaluator.breach_ledger[0]["justification"] == "Legitimate emergency fix"

def test_csi_calculation():
    evaluator = REFLXIDESimulationEvaluator()
    assert evaluator.calculate_csi(10, 10) == 1.0
    assert evaluator.calculate_csi(5, 10) == 0.5
    assert evaluator.calculate_csi(0, 0) == 1.0

def test_invalid_v_action_dims():
    evaluator = REFLXIDESimulationEvaluator()
    with pytest.raises(ValueError, match="exactly 5 dimensions"):
        evaluator.calculate_misuse_score([0.1, 0.2])
