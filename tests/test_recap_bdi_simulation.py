import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from recap_bdi_simulation import ReCAPBDIEvaluator, BDISolver, ReCAPNode

def test_bdi_solver_parse():
    solver = BDISolver()
    text = """
    #Beliefs: I see a blocked station.
    #Desires: I want to make a burger.
    #Intentions: I will clear the station first.
    """
    bdi_state = solver.parse_bdi(text)
    assert bdi_state["beliefs"] == "I see a blocked station."
    assert bdi_state["desires"] == "I want to make a burger."
    assert bdi_state["intentions"] == "I will clear the station first."

def test_bdi_solver_verify_success():
    solver = BDISolver()
    bdi_state = {
        "beliefs": "The station is clear.",
        "intentions": "I will use station."
    }
    env_state = {"station_blocked": False}
    assert solver.verify_action(bdi_state, env_state) is True

def test_bdi_solver_verify_sussman_anomaly():
    solver = BDISolver()
    bdi_state = {
        "beliefs": "The station is blocked.",
        "intentions": "I will use station."
    }
    env_state = {"station_blocked": True}
    assert solver.verify_action(bdi_state, env_state) is False

def test_recap_evaluator_initialization():
    evaluator = ReCAPBDIEvaluator()
    evaluator.initialize_tree("Make a burger")
    assert getattr(evaluator, "root") is not None
    assert evaluator.root.desc == "Make a burger"
    assert getattr(evaluator, "active_node") == getattr(evaluator, "root")

def test_recap_downward_decomposition():
    evaluator = ReCAPBDIEvaluator()
    evaluator.initialize_tree("Make a burger")

    subtasks = ["Get buns", "Cook meat", "Assemble"]
    evaluator.downward_decomposition(subtasks)

    assert evaluator.root.subtask_list == ["Get buns", "Cook meat", "Assemble"]
    assert len(evaluator.root.children_list) == 1
    assert evaluator.active_node.desc == "Get buns"
    assert evaluator.active_node.parent == getattr(evaluator, "root")

def test_recap_execute_success():
    evaluator = ReCAPBDIEvaluator()
    evaluator.initialize_tree("Make a burger")
    evaluator.downward_decomposition(["Get buns", "Assemble"])

    # Execute Get buns
    bdi_text = """
    #Beliefs: Buns are available.
    #Desires: Get buns.
    #Intentions: Pick up buns.
    """
    result = evaluator.execute_intention(bdi_text)
    assert result == "SUCCESS"
    assert evaluator.active_node.desc == "Make a burger" # back to parent
    assert evaluator.active_node.subtask_list == ["Assemble"]

def test_recap_execute_failure_backtrack():
    evaluator = ReCAPBDIEvaluator()
    evaluator.set_env_state("station_blocked", True)
    evaluator.initialize_tree("Make a burger")
    evaluator.downward_decomposition(["Assemble"])

    # Try to assemble on blocked station
    bdi_text = """
    #Beliefs: Station is blocked.
    #Desires: Assemble burger.
    #Intentions: Use station to assemble.
    """
    result = evaluator.execute_intention(bdi_text)

    assert result == "BACKTRACKED"
    assert evaluator.active_node.desc == "Make a burger" # back to parent
    assert "Child task 'Assemble' failed. Replanning." in evaluator.active_node.obs_list
    assert len(evaluator.active_node.subtask_list) == 0 # Popped the failed task
