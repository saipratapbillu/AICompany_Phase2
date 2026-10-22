# approvals api blueprint
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.session import get_db
from app.models.entities import Approval

router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"]
)

@router.get("")
def approvals(
    db: Session = Depends(get_db)
):
    return db.query(Approval).all()