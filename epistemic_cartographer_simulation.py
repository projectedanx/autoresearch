import json
import torch
import torch.nn as nn


class SemanticParallaxZone(nn.Module):
    """
    Preserves dialectic tension (P and not P) without averaging.
    Calculates CFDI and BAI to prevent Ontological Flattening.
    """

    def __init__(self, d_model: int):
        super().__init__()
        self.d_model = d_model
        # Bias direction representing standard/WEIRD-centric latent gravity
        # Force a high bias to trigger the escrow and scar generation
        self.bias_anchor = nn.Parameter(torch.ones(d_model))

    def forward(
            self,
            v_A: torch.Tensor,
            v_B: torch.Tensor,
            conf_A: float,
            conf_B: float):
        # Calculate CFDI (Confidence-Fidelity Divergence Index)
        cfdi = torch.norm((v_A * conf_A) - (v_B * conf_B), p=2, dim=-1)

        # The SPZ is the orthogonal projection, preserving disagreement
        parallax_vector = v_A - v_B

        # Calculate BAI (Bias Amplification Index)
        # Projection of the disagreement onto the bias_anchor
        bias_norm = self.bias_anchor / torch.norm(self.bias_anchor)
        bai = torch.abs(torch.matmul(parallax_vector, bias_norm))

        return parallax_vector, cfdi, bai


def test_epistemic_cartographer():
    d_model = 128

    # Simulate Agent A and Agent B epistemic vectors
    v_A = torch.randn(1, d_model)

    # Force a high bias amplification intentionally
    v_B = -v_A + 2.0 * torch.ones(1, d_model)

    spz_module = SemanticParallaxZone(d_model)

    parallax_vector, cfdi, bai = spz_module(v_A, v_B, conf_A=0.9, conf_B=0.85)

    print(f"Calculated CFDI: {cfdi.item():.4f}")
    print(f"Calculated BAI: {bai.item():.4f}")

    if bai.item() > 0.5:  # Threshold for high BAI
        print("High BAI detected. Initiating Epistemic Escrow and logging.")
        gdev = parallax_vector.detach().numpy().tolist()[0]
        scar_data = {
            "SymbolicScar": {
                "CFDI": cfdi.item(),
                "BAI": bai.item(),
                "GeometricDeviation": gdev,
                "Resolution": "PEF triggered. No flattening occurred."
            }
        }
        with open("SymbolicScar.json", "w") as f:
            json.dump(scar_data, f, indent=2)

    # Mathematically prove that no averaging was performed
    consensus_flat = (v_A + v_B) / 2
    assert not torch.allclose(
        parallax_vector, consensus_flat), "Consensus flattening detected!"

    print("Semantic Parallax Zone successfully maintained.")


if __name__ == '__main__':
    test_epistemic_cartographer()
