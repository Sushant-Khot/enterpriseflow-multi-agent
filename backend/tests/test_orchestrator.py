from backend.app.agents.orchestrator import classify_request


def test_blog_routes_to_a1():
    decision = classify_request("Please review my AWS blog")
    assert decision.intent == "BLOG_REVIEW"
    assert decision.agent == "A1_BLOG"


def test_background_routes_to_a2():
    decision = classify_request("Run a background verification")
    assert decision.intent == "BACKGROUND_CHECK"
    assert decision.agent == "A2_BACKGROUND"


def test_salary_routes_to_a3():
    decision = classify_request("Calculate my monthly incentive")
    assert decision.intent == "SALARY_INCENTIVE"
    assert decision.agent == "A3_SALARY"


def test_unknown_routes_to_support():
    decision = classify_request("I need help with something else")
    assert decision.intent == "GENERAL_SUPPORT"
    assert decision.agent == "A4_SUPPORT"
