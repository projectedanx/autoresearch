from nextjs_frontend_simulation import NextjsFrontendEvaluator


def test_evaluate_dccd_schema_guard_success():
    evaluator = NextjsFrontendEvaluator()
    data = {"agent_intent": "test", "user_context": {}}
    assert evaluator.evaluate_dccd_schema_guard("ComponentAST", data) is True


def test_evaluate_dccd_schema_guard_failure():
    evaluator = NextjsFrontendEvaluator()
    data = {"user_context": {}}
    assert evaluator.evaluate_dccd_schema_guard("ComponentAST", data) is False
    assert evaluator.evaluate_dccd_schema_guard(
        "UnknownSchema", data) is False


def test_route_request_cipher():
    evaluator = NextjsFrontendEvaluator()
    data = {"agent_intent": "security check",
            "user_context": {"role": "admin"}}
    result = evaluator.route_request("user_1", data)
    assert result.get("success") is True
    assert result.get("routed_agent") == "cipher"


def test_route_request_dax_01():
    evaluator = NextjsFrontendEvaluator()
    data = {"agent_intent": "developer support",
            "user_context": {"role": "dev"}}
    result = evaluator.route_request("user_2", data)
    assert result.get("success") is True
    assert result.get("routed_agent") == "dax-01"


def test_route_request_kira_7():
    evaluator = NextjsFrontendEvaluator()
    data = {"agent_intent": "validation logic",
            "user_context": {"role": "system"}}
    result = evaluator.route_request("user_3", data)
    assert result.get("success") is True
    assert result.get("routed_agent") == "kira-7"


def test_route_request_vulcan_fallback():
    evaluator = NextjsFrontendEvaluator()
    data = {"agent_intent": "build microservices",
            "user_context": {"role": "architect"}}
    result = evaluator.route_request("user_4", data)
    assert result.get("success") is True
    assert result.get("routed_agent") == "vulcan"


def test_adjectival_bound_exceeded():
    evaluator = NextjsFrontendEvaluator()
    data = {"agent_intent": "fast amazing seamless solution",
            "user_context": {}}
    result = evaluator.route_request("user_5", data)
    assert "error" in result
    assert "AdjectivalBound exceeded" in result["error"]


def test_route_request_dccd_failure():
    evaluator = NextjsFrontendEvaluator()
    data = {"agent_intent": "test"}  # Missing user_context
    result = evaluator.route_request("user_6", data)
    assert "error" in result
    assert "DCCDSchemaGuard validation failed" in \
        result["error"]
