from typing import Collection


ROLES = {
    "EMPLOYEE",
    "HR_ADMIN",
    "SUPPORT_ADMIN",
}

ROLE_PERMISSIONS: dict[str, set[str]] = {
    "EMPLOYEE": {
        "blog.submit",
        "salary.self",
        "support.create",
    },
    "HR_ADMIN": {
        "background.check",
        "salary.report",
        "approval.manage",
        "blog.submit",
        "support.create",
    },
    "SUPPORT_ADMIN": {
        "support.create",
        "support.read",
        "support.update",
        "support.resolve",
    },
}

INTENT_PERMISSIONS = {
    "BLOG_REVIEW": "blog.submit",
    "BACKGROUND_CHECK": "background.check",
    "SALARY_INCENTIVE": "salary.self",
    "SUPPORT_TICKET": "support.create",
}


def has_permission(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())


def allowed_intent(
    role: str,
    intent: str,
    employee_id: str | None = None,
    user_id: str | None = None,
) -> bool:
    permission = INTENT_PERMISSIONS.get(intent)

    if permission is None:
        return False

    if intent == "SALARY_INCENTIVE" and role == "HR_ADMIN":
        return True

    if not has_permission(role, permission):
        return False

    if intent == "SALARY_INCENTIVE" and role == "EMPLOYEE":
        return employee_id in (None, user_id)

    return True


def require_permission(role: str, permission: str) -> None:
    if not has_permission(role, permission):
        raise PermissionError(
            f"Role {role} is not authorized for {permission}."
        )


def require_any_role(role: str, roles: Collection[str]) -> None:
    if role not in roles:
        expected = ", ".join(sorted(roles))
        raise PermissionError(
            f"Role {role} is not authorized. Required role: {expected}."
        )
