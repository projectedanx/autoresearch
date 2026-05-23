import pytest
from aegis_11_simulation import AEGIS11Evaluator


def test_parse_hickam_topology_success():
    evaluator = AEGIS11Evaluator()
    data = {
        "Hickam_Orientation": "test",
        "Contrastive_Delta": "test",
        "Martensite_Metrics": "test",
        "Consilience_Status": "Pass"
    }
    assert evaluator.parse_hickam_topology(data) is True


def test_parse_hickam_topology_failure():
    evaluator = AEGIS11Evaluator()
    data = {
        "Hickam_Orientation": "test",
        "Contrastive_Delta": "test"
    }
    assert evaluator.parse_hickam_topology(data) is False


def test_calculate_cfdi():
    evaluator = AEGIS11Evaluator()
    assert evaluator.calculate_cfdi(0, 0.5) == 1.0
    assert evaluator.calculate_cfdi(1.0, 0.1) == 0.1


def test_apply_golden_ratio_synthesis():
    evaluator = AEGIS11Evaluator()
    res = evaluator.apply_golden_ratio_synthesis(10.0, 5.0)
    assert res == (10.0 * 1.618) + (5.0 * 1.0)


def test_calculate_cosine_similarity():
    evaluator = AEGIS11Evaluator()
    with pytest.raises(ValueError):
        evaluator.calculate_cosine_similarity([1.0], [1.0, 2.0])

    with pytest.raises(ValueError):
        evaluator.calculate_cosine_similarity([], [])

    vec1 = [1.0, 0.0]
    vec2 = [0.0, 1.0]
    assert evaluator.calculate_cosine_similarity(vec1, vec2) == 0.0

    vec3 = [1.0, 0.0]
    vec4 = [1.0, 0.0]
    assert evaluator.calculate_cosine_similarity(vec3, vec4) == 1.0


def test_calculate_cosine_similarity_zero_norm():
    evaluator = AEGIS11Evaluator()
    assert evaluator.calculate_cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0


def test_evaluate_exit_gate_success():
    evaluator = AEGIS11Evaluator()
    # IAR = 98/100 = 0.98
    # SDS = 1 - 0.96 = 0.04 (<= 0.05)
    # Cosine Similarity = 0.96
    # Let target_vec = [1, 0, 0], generated_vec = [0.96, 0.28, 0]
    # -> length = sqrt(0.96^2 + 0.28^2) = 1.0
    target = [1.0, 0.0, 0.0]
    generated = [0.96, 0.28, 0.0]
    assert evaluator.evaluate_exit_gate(98, 100, target, generated) is True


def test_evaluate_exit_gate_failure_iar():
    evaluator = AEGIS11Evaluator()
    # IAR = 97/100 = 0.97
    target = [1.0, 0.0]
    generated = [1.0, 0.0]
    assert evaluator.evaluate_exit_gate(97, 100, target, generated) is False


def test_evaluate_exit_gate_failure_sds():
    evaluator = AEGIS11Evaluator()
    # IAR = 100/100 = 1.0
    # SDS = 1 - 0.0 = 1.0
    target = [1.0, 0.0]
    generated = [0.0, 1.0]
    assert evaluator.evaluate_exit_gate(100, 100, target, generated) is False


def test_evaluate_exit_gate_zero_constraints():
    evaluator = AEGIS11Evaluator()
    with pytest.raises(ValueError):
        evaluator.evaluate_exit_gate(0, 0, [1.0], [1.0])


def test_check_cfdi_limit():
    evaluator = AEGIS11Evaluator()
    assert evaluator.check_cfdi_limit(0.12) is True
    assert evaluator.check_cfdi_limit(0.0812) is True
    assert evaluator.check_cfdi_limit(0.13) is False


def test_extract_separable_grid():
    evaluator = AEGIS11Evaluator()
    inputs = {
        "var_a": 1,
        "mut_state": "changed",
        "eff_log": "error",
        "other": "ignore"
    }
    grid = evaluator.extract_separable_grid(inputs)
    assert "var_a" in grid["variables"]
    assert ("mut_state", "changed") in grid["state_mutations"]
    assert ("eff_log", "error") in grid["side_effects"]
    assert len(grid["variables"]) == 1
    assert len(grid["state_mutations"]) == 1
    assert len(grid["side_effects"]) == 1


if __name__ == "__main__":
    pytest.main()
