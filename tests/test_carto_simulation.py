import pytest
from carto_simulation import CartoTopologyEvaluator

def test_carto_betti_1_detection():
    evaluator = CartoTopologyEvaluator()
    # Linear DAG
    clean_graph = {
        'build': ['test'],
        'test': ['deploy'],
        'deploy': []
    }
    cycles = evaluator.calculate_betti_1_cycles(clean_graph)
    assert cycles == 0
    assert evaluator.check_epistemic_escrow() == "PASS"

def test_carto_epistemic_escrow_halt():
    evaluator = CartoTopologyEvaluator()
    # Circular DAG
    cycle_graph = {
        'build': ['test'],
        'test': ['deploy'],
        'deploy': ['build']
    }
    evaluator.calculate_betti_1_cycles(cycle_graph)
    with pytest.raises(ValueError, match="Betti-1 cycle detected"):
        evaluator.check_epistemic_escrow()

def test_carto_gds_halt():
    evaluator = CartoTopologyEvaluator()
    evaluator.ground_truth_delta_score = 0.4
    with pytest.raises(ValueError, match="GDS < 0.5"):
        evaluator.check_epistemic_escrow()

def test_carto_pdi_warning():
    evaluator = CartoTopologyEvaluator()
    evaluator.pluriversal_drift_index = 0.4
    assert evaluator.check_epistemic_escrow() == "WARNING: Activate Golden Scar preservation protocol."
