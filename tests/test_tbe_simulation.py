import pytest
from tbe_simulation import State, Action, TemporalBlendingEngineEvaluator

def test_evaluate_transition():
    evaluator = TemporalBlendingEngineEvaluator()
    s_k = State(fluents={"f_cam": 1, "f_door": 0})
    a_k = Action(name="disable_cam", preconditions={}, effects={"f_cam": 0})

    # Valid transition
    s_k_plus_1_valid = State(fluents={"f_cam": 0, "f_door": 0})
    assert evaluator.evaluate_transition(s_k, a_k, s_k_plus_1_valid) == True

    # Invalid transition (precondition fails - if we had one)
    a_k_with_pre = Action(name="disable_cam", preconditions={"f_cam": 1}, effects={"f_cam": 0})
    assert evaluator.evaluate_transition(s_k, a_k_with_pre, s_k_plus_1_valid) == True

    s_k_invalid_pre = State(fluents={"f_cam": 0, "f_door": 0})
    assert evaluator.evaluate_transition(s_k_invalid_pre, a_k_with_pre, s_k_plus_1_valid) == False

    # Invalid transition (effect fails)
    s_k_plus_1_invalid_eff = State(fluents={"f_cam": 1, "f_door": 0})
    assert evaluator.evaluate_transition(s_k, a_k, s_k_plus_1_invalid_eff) == False

    # Invalid transition (frame operator fails)
    s_k_plus_1_invalid_frame = State(fluents={"f_cam": 0, "f_door": 1})
    assert evaluator.evaluate_transition(s_k, a_k, s_k_plus_1_invalid_frame) == False


def test_calculate_cpi_theorem_3_1():
    """
    Formally verify Theorem 3.1: The Cascading Contradiction Boundary
    If a sequence contains a single causal contradiction, CPI will drop.
    To satisfy CPI >= 0.95, the sequence must be at least N=21 states (N-1 >= 20 actions)
    if exactly one action fails.
    """
    evaluator = TemporalBlendingEngineEvaluator()

    # Let's create a trace where exactly 1 transition fails.
    # N states, N-1 actions
    # We will simulate the "Security Camera Lemma"

    # Initial state: camera is ON
    states = [State(fluents={"f_cam": 1})]
    actions = []

    # Step 1: disable camera
    actions.append(Action(name="disable_cam", preconditions={}, effects={"f_cam": 0}))
    states.append(State(fluents={"f_cam": 0}))

    # Suppose we want to construct a trace of length N states.
    # We add (N - 3) valid dummy actions where camera remains OFF
    # And 1 invalid action at the end where we assume camera is ON but it's OFF

    def generate_trace_with_one_error(N: int):
        trace_states = [State(fluents={"f_cam": 1})]
        trace_actions = []

        # Action 1: disable camera
        trace_actions.append(Action(name="disable_cam", preconditions={}, effects={"f_cam": 0}))
        trace_states.append(State(fluents={"f_cam": 0}))

        # Action 2 to N-2: dummy actions that maintain frame
        for i in range(2, N - 1):
            trace_actions.append(Action(name=f"dummy_{i}", preconditions={}, effects={}))
            trace_states.append(State(fluents={"f_cam": 0}))

        # Action N-1: The error action! Demands camera ON, but it is OFF
        trace_actions.append(Action(name="need_cam", preconditions={"f_cam": 1}, effects={}))
        trace_states.append(State(fluents={"f_cam": 0})) # State transitions but indicator is 0

        return trace_states, trace_actions

    # N=20 -> 1 error in 19 transitions -> CPI = 18/19 = 0.947 < 0.95 (FAIL)
    states_20, actions_20 = generate_trace_with_one_error(20)
    cpi_20 = evaluator.calculate_cpi(states_20, actions_20)
    assert cpi_20 == 18.0 / 19.0
    assert cpi_20 < 0.95

    # N=21 -> 1 error in 20 transitions -> CPI = 19/20 = 0.95 >= 0.95 (PASSes the contradiction bound)
    states_21, actions_21 = generate_trace_with_one_error(21)
    cpi_21 = evaluator.calculate_cpi(states_21, actions_21)
    assert cpi_21 == 19.0 / 20.0
    assert cpi_21 >= 0.95


def test_epistemic_rheological_stability():
    """
    Verify Epistemic Rheological Stability bounds
    """
    evaluator = TemporalBlendingEngineEvaluator()

    # If delta_t = 1.0, mu = 10.0, f_constraint_norm = 5.0, delta = 1.0
    # L = 5.0 / 10.0 = 0.5
    # displacement = 0.5 * 1.0 = 0.5 < 1.0 (delta) -> True
    assert evaluator.check_epistemic_rheological_stability(delta_t=1.0, mu=10.0, f_constraint_norm=5.0, delta=1.0) == True

    # If mu is lower (viscosity drops), displacement increases
    # mu = 2.0 -> L = 5.0 / 2.0 = 2.5
    # displacement = 2.5 * 1.0 = 2.5 > 1.0 (delta) -> False
    assert evaluator.check_epistemic_rheological_stability(delta_t=1.0, mu=2.0, f_constraint_norm=5.0, delta=1.0) == False

    with pytest.raises(ValueError):
        evaluator.check_epistemic_rheological_stability(delta_t=1.0, mu=0.0, f_constraint_norm=5.0, delta=1.0)


def test_tension_frontier():
    evaluator = TemporalBlendingEngineEvaluator()
    cch, csd, optimal = evaluator.evaluate_tension_frontier(
        verification_depth=10, tokens=1000,
        temperature=0.7, variance=5.0,
        budget_threshold=4.0
    )
    assert cch == 10000.0
    assert csd == 3.5
    assert optimal == True

    cch, csd, optimal = evaluator.evaluate_tension_frontier(
        verification_depth=10, tokens=1000,
        temperature=0.9, variance=5.0,
        budget_threshold=4.0
    )
    assert csd == 4.5
    assert optimal == False
