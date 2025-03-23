from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user
from typing import List

def require_role(allowed_roles: List[str]):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role.name.lower() not in [role.lower() for role in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker
