from fastapi import Depends, status, HTTPException
from adapters.shared.token import get_current_user_payload

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, payload: dict = Depends(get_current_user_payload)) -> dict:
        user_role = payload.get("role")

        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас нет прав на это действие"
            )

        return payload