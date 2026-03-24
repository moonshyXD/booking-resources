from fastapi import Depends, HTTPException, status


def RoleChecker(allowed_roles: list, user_getter: callable):
    async def check_permissions(user_payload: dict = Depends(user_getter)):
        user_role = user_payload.get("role")

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения операции"
            )

        return user_payload

    return check_permissions
