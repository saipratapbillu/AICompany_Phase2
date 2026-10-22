# users api blueprint
import uuid

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import AppUser
from app.schemas.schemas import UserRegister

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register")
def register_user(
    body: UserRegister,
    db: Session = Depends(get_db)
):

    user = AppUser(

        UserID=uuid.uuid4(),

        Email=body.email,

        PasswordHash=body.password,

        DisplayName=
        f"{body.first_name} {body.last_name}",

        Department=body.department,

        IsActive=True,

        RoleID='00000000-0000-0000-0000-000000000001'
    )

    db.add(user)

    db.commit()

    return {
        "message":"User registered successfully"
    }