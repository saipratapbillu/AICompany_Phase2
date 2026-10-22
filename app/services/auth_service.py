import uuid
from sqlalchemy import select
from fastapi import HTTPException

from app.models.entities import AppUser


class AuthService:

    def authenticate(
        self,
        db,
        email: str,
        password: str
    ):

        user = db.execute(
            select(AppUser)
            .where(AppUser.Email == email)
        ).scalar_one_or_none()

        if not user:
            raise HTTPException(
                401,
                "Invalid credentials"
            )

        # Replace later with bcrypt
        if user.PasswordHash != password:
            raise HTTPException(
                401,
                "Invalid credentials"
            )

        return {
            "user_id": str(user.UserID),
            "email": user.Email,
            "display_name": user.DisplayName
        }