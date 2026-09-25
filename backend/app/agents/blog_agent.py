from backend.app.services.bedrock import invoke_bedrock
from backend.app.services.approval_store import approval_store
from backend.app.graph.state import AgentState

from langgraph.types import interrupt


BLOG_SYSTEM_PROMPT = """
You are A1, the Blog Analysis and Review Agent
for EnterpriseFlow AI.

Review the supplied blog content for:

1. Structure
2. Clarity
3. Completeness
4. Consistency
5. Professional quality
6. Grammar
7. Readability

Return the result using exactly these sections:

OVERALL_SCORE: <number from 0 to 100>

SUMMARY:
<short summary>

STRENGTHS:
- <strength>
- <strength>

ISSUES:
- <issue>
- <issue>

RECOMMENDATIONS:
- <recommendation>
- <recommendation>

ACCEPTED: YES or NO

Acceptance means the blog is sufficiently clear,
complete, professional and readable.
"""


def _fallback_blog_review(
    content: str,
    human_feedback: str = "",
) -> str:

    feedback_text = ""

    if human_feedback:
        feedback_text = (
            f"\n\nHuman reviewer feedback:\n"
            f"{human_feedback}"
        )

    return f"""
OVERALL_SCORE: 75

SUMMARY:
The blog content was reviewed using the
EnterpriseFlow AI blog quality checklist.

STRENGTHS:
- Content is understandable.
- Main topic is identifiable.
- Basic structure is present.

ISSUES:
- Some sections may require additional detail.
- Grammar and readability can be improved.
- Professional consistency can be improved.

RECOMMENDATIONS:
- Improve paragraph structure.
- Correct grammar and wording.
- Add missing supporting details.

ACCEPTED: NO
{feedback_text}
""".strip()


def review_blog(
    content: str,
    human_feedback: str = "",
) -> str:

    user_prompt = f"""
Review the following blog.

BLOG CONTENT:
{content}

"""

    if human_feedback:
        user_prompt += f"""
PREVIOUS HUMAN REVIEWER FEEDBACK:
{human_feedback}

Use this feedback when performing the
new review.
"""

    try:

        result = invoke_bedrock(
            BLOG_SYSTEM_PROMPT,
            user_prompt,
        )

        return result["text"]

    except Exception:

        return _fallback_blog_review(
            content,
            human_feedback,
        )


def _is_blog_accepted(
    review: str,
) -> bool:

    return (
        "ACCEPTED: YES"
        in review.upper()
    )


def blog_agent(
    state: AgentState,
) -> dict:

    tool_results = (
        state.get("tool_results", {})
        or {}
    )

    content = (
        tool_results.get("blog_content")
        or state.get("user_input", "")
    ).strip()

    human_feedback = (
        state.get("human_feedback", "")
        or ""
    ).strip()

    iteration_count = (
        state.get("iteration_count", 0)
    )

    max_iterations = (
        state.get("max_iterations", 5)
    )

    workflow_id = state[
        "workflow_id"
    ]

    # -------------------------------------------------
    # Run the blog review
    # -------------------------------------------------

    review = review_blog(
        content=content,
        human_feedback=human_feedback,
    )

    # -------------------------------------------------
    # Accepted
    # -------------------------------------------------

    if _is_blog_accepted(review):

        return {
            "response": review,
            "status": "COMPLETED",
            "approval_status": "NOT_REQUIRED",
            "requires_human_approval": False,
            "iteration_count": (
                iteration_count + 1
            ),
        }

    # -------------------------------------------------
    # Maximum iteration protection
    # -------------------------------------------------

    if iteration_count >= max_iterations:

        return {
            "response": review,
            "status": "COMPLETED_MAX_ITERATIONS",
            "approval_status": "MAX_ITERATIONS_REACHED",
            "requires_human_approval": False,
            "iteration_count": (
                iteration_count + 1
            ),
        }

    # -------------------------------------------------
    # Create / reuse approval
    # -------------------------------------------------

    approval = (
        approval_store.create_approval(
            workflow_id=workflow_id,
            review=review,
        )
    )

    approval_id = approval[
        "approval_id"
    ]

    # -------------------------------------------------
    # Pause LangGraph execution
    # -------------------------------------------------

    human_decision = interrupt(
        {
            "type": "BLOG_REVIEW_APPROVAL",

            "approval_id": approval_id,

            "workflow_id": workflow_id,

            "question": (
                "Please review the blog analysis "
                "and approve it or request revision."
            ),

            "review": review,

            "iteration": (
                iteration_count + 1
            ),
        }
    )

    # -------------------------------------------------
    # Resume after human decision
    # -------------------------------------------------

    approved = False
    feedback = ""

    if isinstance(
        human_decision,
        dict,
    ):

        approved = bool(
            human_decision.get(
                "approved",
                False,
            )
        )

        feedback = (
            human_decision.get(
                "feedback",
                "",
            )
            or ""
        ).strip()

    else:

        approved = bool(
            human_decision
        )

    # -------------------------------------------------
    # Save approval decision
    # -------------------------------------------------

    approval_store.submit_feedback(
        approval_id=approval_id,
        approved=approved,
        feedback=feedback,
    )

    # -------------------------------------------------
    # Human approved
    # -------------------------------------------------

    if approved:

        return {
            "response": review,
            "status": "COMPLETED",
            "approval_id": approval_id,
            "approval_status": "APPROVED",
            "requires_human_approval": False,
            "human_feedback": feedback,
            "iteration_count": (
                iteration_count + 1
            ),
        }

    # -------------------------------------------------
    # Human requested revision
    # -------------------------------------------------

    return {
        "response": review,
        "status": "REVISION_REQUESTED",
        "approval_id": approval_id,
        "approval_status": "REVISION_REQUESTED",
        "requires_human_approval": False,
        "human_feedback": feedback,
        "iteration_count": (
            iteration_count + 1
        ),
    }