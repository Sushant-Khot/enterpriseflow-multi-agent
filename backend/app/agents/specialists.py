"""
Compatibility layer for specialist agents.

The actual implementation for each specialist lives in:
    blog_agent.py
    background_agent.py
    salary_agent.py
    support_agent.py
"""

from backend.app.agents.blog_agent import blog_agent
from backend.app.agents.background_agent import background_agent
from backend.app.agents.salary_agent import salary_agent
from backend.app.agents.support_agent import support_agent


__all__ = [
    "blog_agent",
    "background_agent",
    "salary_agent",
    "support_agent",
]