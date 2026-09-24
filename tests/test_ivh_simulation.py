import pytest
import math
from src.ivh_simulation import (
    AnomalyMiningModule,
    SymbolicEquationSolver,
    ExplanatoryGraphStructurer,
    PopperianEdgeCaseFalsifier,
    OccamLossCompiler,
    CognitiveArchitectureCompiler,
    DeIdealizationEngine,
    IVHEvaluator
)

def test_anomaly_mining_module():
    miner = AnomalyMiningModule(threshold_sigma=3.0)

    # Test sigma calculation
    assert miner.calculate_sigma_divergence(10.0, 10.0, 2.0) == 0.0
    assert miner.calculate_sigma_divergence(10.0, 16.0, 2.0) == 3.0
    assert miner.calculate_sigma_divergence(10.0, 17.0, 2.0) == 3.5

    # Test zero std dev edge case
    assert miner.calculate_sigma_divergence(10.0, 10.0, 0.0) == 0.0
    assert miner.calculate_sigma_divergence(10.0, 11.0, 0.0) == float('inf')

    # Test screen_data
    data_stream = [
        {"x": 1.0, "target_val": 2.0},
        {"x": 2.0, "target_val": 4.0},
        {"x": 3.0, "target_val": 15.0} # Anomaly
    ]
    current_paradigm = {
        "predict_func": lambda dp: dp["x"] * 2.0,
        "std_dev": 1.0
    }

    anomalies = miner.screen_data(data_stream, current_paradigm)
    assert len(anomalies) == 1
    assert anomalies[0]["observed"] == 15.0
    assert anomalies[0]["sigma_divergence"] == 9.0

def test_symbolic_equation_solver():
    solver = SymbolicEquationSolver()

    res1 = solver.translate_to_schema("We observed a general pattern.")
    assert res1["status"] == "rejected"
    assert res1["reason"] == "vague generalization"

    res2 = solver.translate_to_schema("This describes a coordinate-free tensor field.")
    assert res2["status"] == "accepted"
    assert res2["schema"] == "formal_law"

    res3 = solver.translate_to_schema("It is a closed-form differential equation.")
    assert res3["status"] == "accepted"

def test_explanatory_graph_structurer():
    structurer = ExplanatoryGraphStructurer()

    aic1 = structurer.calculate_aic(k=3, max_likelihood=0.5)
    assert math.isclose(aic1, 2*3 - 2*math.log(0.5))

    # Edge case: non-positive likelihood
    assert structurer.calculate_aic(k=3, max_likelihood=0.0) == float('inf')

def test_popperian_falsifier():
    falsifier = PopperianEdgeCaseFalsifier()

    law = {"type": "Newtonian", "equation": "F=ma"}
    res = falsifier.evaluate_asymptotic_limit(law, "v -> c")
    assert res["status"] == "falsified"

    res2 = falsifier.evaluate_asymptotic_limit(law, "v << c")
    assert res2["status"] == "verified"

def test_occam_loss_compiler():
    compiler = OccamLossCompiler()

    bic = compiler.calculate_bic(k=2, n=100, max_likelihood=0.8)
    assert math.isclose(bic, 2*math.log(100) - 2*math.log(0.8))

    # Edge cases
    assert compiler.calculate_bic(k=2, n=0, max_likelihood=0.8) == float('inf')
    assert compiler.calculate_bic(k=2, n=100, max_likelihood=-1.0) == float('inf')

    model_a = {"k": 20, "max_likelihood": 0.99} # Complex
    model_b = {"k": 2, "max_likelihood": 0.95}  # Parsimonious

    res = compiler.compare_models(model_a, model_b, n=1000)
    assert "Model B preferred" in res

def test_cognitive_architecture_compiler():
    compiler = CognitiveArchitectureCompiler()

    score = compiler.evaluate_grasping_metric(True, False, False)
    assert math.isclose(score, 0.3)

    score_full = compiler.evaluate_grasping_metric(True, True, True)
    assert math.isclose(score_full, 1.0)

def test_de_idealization_engine():
    engine = DeIdealizationEngine()

    model_dag = {"assumptions": "point mass, zero friction", "dimensionality": 2}
    test_data = [{"friction": 0.1}, {"friction": 0.8}] # 0.8 > 0.5 triggers audit

    audit_res = engine.audit_boundaries(model_dag, test_data)
    assert audit_res["status"] == "divergence_detected"
    assert audit_res["faulty_assumption"] == "zero friction"

    new_model = engine.execute_de_idealization(model_dag, audit_res["faulty_assumption"])
    assert "zero friction" not in new_model["assumptions"]
    assert new_model["dimensionality"] == 3

    # Test OK path
    test_data_ok = [{"friction": 0.1}, {"friction": 0.2}]
    audit_res_ok = engine.audit_boundaries(model_dag, test_data_ok)
    assert audit_res_ok["status"] == "ok"

def test_ivh_evaluator():
    evaluator = IVHEvaluator()
    assert isinstance(evaluator.anomaly_miner, AnomalyMiningModule)
    assert isinstance(evaluator.symbolic_solver, SymbolicEquationSolver)
    assert isinstance(evaluator.graph_structurer, ExplanatoryGraphStructurer)
    assert isinstance(evaluator.falsifier, PopperianEdgeCaseFalsifier)
    assert isinstance(evaluator.occam_compiler, OccamLossCompiler)
    assert isinstance(evaluator.cognitive_compiler, CognitiveArchitectureCompiler)
    assert isinstance(evaluator.de_idealization_engine, DeIdealizationEngine)
