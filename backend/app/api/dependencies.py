from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from app.core.security import verify_token

# Swagger needs the exact relative path for the token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user_token(token: str = Depends(oauth2_scheme)):
    """
    Dependency that decodes the JWT and returns the user payload.
    """
    return verify_token(token)

class RoleChecker:
    """
    Dependency class to enforce strict Role-Based Access Control (RBAC).
    HIPAA § 164.312(a)(1) - Access Control.
    """
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict = Depends(get_current_user_token)):
        # If there's no role in the token, or it's not allowed, block access
        if not user.get("role") or user.get("role") not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required roles: {', '.join(self.allowed_roles)}"
            )
        return user
