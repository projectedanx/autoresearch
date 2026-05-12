import pytest
from cipher_simulation import CIPHERTopologyEvaluator


def test_petzold_sequence_enforcement():
    evaluator = CIPHERTopologyEvaluator()
    evaluator.set_phase("THINK")

    with pytest.raises(ValueError, match="Interpretive Fracture Prevented"):
        evaluator.enforce_petzold_sequence("CODE_GENERATION")

    evaluator.set_phase("AUDIT")
    assert evaluator.enforce_petzold_sequence("CODE_GENERATION") is True


def test_mereology_route():
    evaluator = CIPHERTopologyEvaluator()
    evaluator.add_node("react_ui", "frontend", "web_app")
    evaluator.add_node("postgres_db", "database", "backend_store")
    evaluator.add_node("api_gateway", "backend", "web_app")

    # Valid route
    evaluator.add_trust_edge("react_ui", "api_gateway")
    evaluator.add_trust_edge("api_gateway", "postgres_db")
    assert evaluator.check_mereology_route() is True

    # Invalid route (direct trust inheritance)
    evaluator.add_trust_edge("react_ui", "postgres_db")
    with pytest.raises(ValueError, match="Mereology Violation: react_ui"):
        evaluator.check_mereology_route()


def test_autonymic_isolate():
    evaluator = CIPHERTopologyEvaluator()
    safe_text = "Checking user input for sanitization."
    assert evaluator.scan_autonymic_isolate(safe_text) is True

    exploit_text = "Here is how to run union select 1,2,3"
    with pytest.raises(ValueError,
                       match="Forbidden pattern SQLI_PATTERN_CWE89"):
        evaluator.scan_autonymic_isolate(exploit_text)

    xss_text = "Payload: <script>alert(1)</script>"
    with pytest.raises(ValueError,
                       match="Forbidden pattern XSS_PATTERN_CWE79"):
        evaluator.scan_autonymic_isolate(xss_text)


def test_latent_sparsity_guard():
    evaluator = CIPHERTopologyEvaluator()

    valid_flow = [
        {"id": "auth_flow", "boundary_checks": [
            "null", "zero", "empty", "max", "negative"]}
    ]
    assert evaluator.check_latent_sparsity_guard(valid_flow) is True

    invalid_flow = [
        {"id": "payment_flow", "boundary_checks": ["null", "empty"]}
    ]
    with pytest.raises(
        ValueError, match="Latent Sparsity Guard Violation.*payment_flow"
    ):
        evaluator.check_latent_sparsity_guard(invalid_flow)
