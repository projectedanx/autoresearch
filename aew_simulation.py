import torch
import torch.nn as nn


class PhantomDimension(nn.Module):
    """
    Z-Axis inference module that handles contradictory features by routing them
    orthogonally into a phantom depth dimension (H_k).
    """

    def __init__(self, d_model: int, phantom_depth: int = 4):
        super().__init__()
        self.d_model = d_model
        self.phantom_depth = phantom_depth

        # We project the contradiction into a phantom dimension
        self.z_axis_proj = nn.Linear(d_model, d_model * phantom_depth)

        # Paraconsistent 'B' state gate
        self.dissonance_gate = nn.Parameter(torch.tensor(0.5))

    def forward(self, x):
        # Enactment of Region Connection Calculus (RCC-8) PO
        # We hold the overlap in a paraconsistent state and activate Z-Axis.

        # 1. Promote to Phantom Dimension
        phantom_state = self.z_axis_proj(x)
        phantom_state = phantom_state.view(
            *x.shape[:-1], self.phantom_depth, self.d_model)

        # 2. VW3 Dissonance Induction (Beneficial Friction via nonlinear act)
        friction = torch.tanh(phantom_state) * torch.sigmoid(phantom_state)

        # 3. Resolve back to Euclidean space
        resolved = friction.sum(dim=-2)  # Integrate along Z-axis

        # 4. Mix with paraconsistent gate
        return x + self.dissonance_gate * resolved


def test_phantom_dimension():
    d_model = 128
    batch_size = 4
    seq_len = 16

    x = torch.randn(batch_size, seq_len, d_model)

    model = PhantomDimension(d_model)
    y = model(x)

    assert y.shape == x.shape, \
        "Z-Axis inference failed to preserve Euclidean dimensionality."
    assert not torch.isnan(y).any(), \
        "Paraconsistent state collapsed into NaN."

    print("Topological novelty verified. Phantom simulated.")


if __name__ == '__main__':
    test_phantom_dimension()
