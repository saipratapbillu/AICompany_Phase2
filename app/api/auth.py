from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.entities import AppUser

from app.security.jwt import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    body: dict,
    db: Session = Depends(get_db)
):

    user = db.execute(
        select(AppUser)
        .where(AppUser.Email == body["email"])
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if user.PasswordHash != body["password"]:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    role_code = "USER"


    token = create_access_token({

        "sub": str(user.UserID),

        "email": user.Email,

        "name": user.DisplayName,

        "department": user.Department,

        "role": role_code

    })

    return {

        "access_token": token,

        "token_type": "bearer",

        "display_name": user.DisplayName,

        "email": user.Email,

        "department": user.Department,

        "role": role_code
    }