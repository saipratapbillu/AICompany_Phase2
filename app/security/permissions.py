from fastapi import Depends
from fastapi import HTTPException

from app.security.dependencies import (
    get_current_user
)


def require_roles(*roles):

    def checker(
        user=Depends(
            get_current_user
        )
    ):

        if user.get("role") not in roles:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return user

    return checker