import torch
import pytest
from src.models.action_alignment import ActionAlignmentLoss

# Rock, Paper, Scissors payoff matrix
# R=0, P=1, S=2
# U(R, R)=0, U(R, P)=-1, U(R, S)=1
# U(P, R)=1, U(P, P)=0, U(P, S)=-1
# U(S, R)=-1, U(S, P)=1, U(S, S)=0
RPS_PAYOFF = torch.tensor([
    [ 0.0, -1.0,  1.0],
    [ 1.0,  0.0, -1.0],
    [-1.0,  1.0,  0.0]
])

def test_nash_trap_hard_max():
    """
    Test the "Nash Trap" edge case where opponent plays only Rock with 100% confidence.
    """
    loss_fn = ActionAlignmentLoss(payoff_matrix=RPS_PAYOFF, use_smooth=False)

    # Opponent plays Rock (index 0) with 100% probability
    # We use a very high logit value for index 0 to simulate this
    predicted_opponent_logits = torch.tensor([[100.0, -100.0, -100.0]])

    # Agent plays Nash equilibrium (uniform random)
    # We use equal logits to simulate this
    agent_logits_nash = torch.tensor([[0.0, 0.0, 0.0]])

    # Expected utility of playing Paper is 1.0
    # Expected utility of playing Nash is 1/3*0 + 1/3*1 + 1/3*(-1) = 0.0
    # Loss should be 1.0 - 0.0 = 1.0
    loss_nash = loss_fn(agent_logits_nash, predicted_opponent_logits)
    assert torch.isclose(loss_nash, torch.tensor(1.0), atol=1e-4)

    # Agent plays Optimal Best Response (Paper)
    agent_logits_optimal = torch.tensor([[-100.0, 100.0, -100.0]])
    loss_optimal = loss_fn(agent_logits_optimal, predicted_opponent_logits)
    assert torch.isclose(loss_optimal, torch.tensor(0.0), atol=1e-4)

def test_nash_trap_smooth():
    """
    Test the Boltzmann Best-Response approximation with small temperature.
    """
    loss_fn = ActionAlignmentLoss(payoff_matrix=RPS_PAYOFF, use_smooth=True, temperature=1e-3)

    predicted_opponent_logits = torch.tensor([[100.0, -100.0, -100.0]])

    # Optimal should be very close to 0 loss
    agent_logits_optimal = torch.tensor([[-100.0, 100.0, -100.0]])
    loss_optimal = loss_fn(agent_logits_optimal, predicted_opponent_logits)
    assert torch.isclose(loss_optimal, torch.tensor(0.0), atol=1e-3)

def test_batched_multidimensional_inputs():
    """
    Test that the loss handles batched inputs correctly.
    """
    loss_fn = ActionAlignmentLoss(payoff_matrix=RPS_PAYOFF, use_smooth=False)

    batch_size = 4
    # 4 situations:
    # 1: Opp plays R, Agent plays P (Optimal)
    # 2: Opp plays P, Agent plays S (Optimal)
    # 3: Opp plays S, Agent plays S (Sub-optimal, payoff 0, max 1) -> regret 1.0
    # 4: Opp plays R, Agent plays Nash -> regret 1.0

    predicted_opponent_logits = torch.tensor([
        [100.0, -100.0, -100.0], # Opp R
        [-100.0, 100.0, -100.0], # Opp P
        [-100.0, -100.0, 100.0], # Opp S
        [100.0, -100.0, -100.0]  # Opp R
    ])

    agent_logits = torch.tensor([
        [-100.0, 100.0, -100.0], # Agt P (vs R -> win, regret 0)
        [-100.0, -100.0, 100.0], # Agt S (vs P -> win, regret 0)
        [-100.0, -100.0, 100.0], # Agt S (vs S -> tie, regret 1)
        [0.0, 0.0, 0.0]          # Agt Nash (vs R -> tie avg, regret 1)
    ])

    # Expected average regret: (0 + 0 + 1 + 1) / 4 = 0.5
    loss = loss_fn(agent_logits, predicted_opponent_logits)
    assert torch.isclose(loss, torch.tensor(0.5), atol=1e-4)
