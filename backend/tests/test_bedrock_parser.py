from backend.app.agents.orchestrator import _extract_json


def test_extract_plain_json():

    text = """
    {
        "intent": "BLOG_REVIEW",
        "agent": "A1_BLOG",
        "confidence": 0.95,
        "reason": "The user wants a blog reviewed."
    }
    """

    result = _extract_json(text)

    assert result["intent"] == "BLOG_REVIEW"
    assert result["agent"] == "A1_BLOG"


def test_extract_markdown_json():

    text = """
    ```json
    {
        "intent": "SALARY_INCENTIVE",
        "agent": "A3_SALARY",
        "confidence": 0.92,
        "reason": "The user asks about salary."
    }
    ```
    """

    result = _extract_json(text)

    assert result["intent"] == "SALARY_INCENTIVE"
    assert result["agent"] == "A3_SALARY"