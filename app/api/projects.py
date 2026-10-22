# projects api blueprint
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from app.security.dependencies import get_current_user
from app.security.permissions import require_roles
from app.db.session import get_db
from app.models.entities import Project

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.get("")
def projects(
    db: Session = Depends(get_db)
):
    return db.query(Project).all()