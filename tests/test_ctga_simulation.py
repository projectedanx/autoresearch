import pytest
from ctga_simulation import CTGAEvaluator

def test_evaluate_betti_1_persistence_pass():
    evaluator = CTGAEvaluator()
    # Should not raise exception
    assert evaluator.evaluate_betti_1_persistence(1.5, 2.0) is True

def test_evaluate_betti_1_persistence_fail():
    evaluator = CTGAEvaluator()
    with pytest.raises(ValueError, match="Epistemic Escrow triggered"):
        evaluator.evaluate_betti_1_persistence(2.5, 2.0)

def test_compute_ssi():
    evaluator = CTGAEvaluator()
    # Normal case: reduced scar by half -> SSI should be 0.5
    assert evaluator.compute_ssi(10.0, 5.0) == 0.5

    # Complete resolution case -> SSI should be 1.0
    assert evaluator.compute_ssi(10.0, 0.0) == 1.0

    # Worse case -> SSI should be negative
    assert evaluator.compute_ssi(10.0, 20.0) == -1.0

    # Initial is zero, final is zero -> SSI should be 1.0
    assert evaluator.compute_ssi(0.0, 0.0) == 1.0

    # Initial is zero, final is positive -> SSI should be -inf
    assert evaluator.compute_ssi(0.0, 5.0) == float('-inf')

def test_detect_concept_collapse():
    evaluator = CTGAEvaluator()
    # Stable or increasing components -> no collapse
    assert evaluator.detect_concept_collapse([5, 5, 5]) is False
    assert evaluator.detect_concept_collapse([1, 2, 3]) is False

    # Decrease in components -> collapse
    assert evaluator.detect_concept_collapse([5, 4, 3]) is True
    assert evaluator.detect_concept_collapse([10, 10, 8, 8]) is True

    # Too short history
    assert evaluator.detect_concept_collapse([5]) is False
    assert evaluator.detect_concept_collapse([]) is False
