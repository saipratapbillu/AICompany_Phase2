from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/dashboard/api",
    tags=["Dashboard"]
)

@router.get("")
def dashboard(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return {

        "requirements":
            db.execute(
                text(
                    "SELECT COUNT(*) FROM Requirement"
                )
            ).scalar(),

        "assessments":
            db.execute(
                text(
                    "SELECT COUNT(*) FROM RequirementAssessment"
                )
            ).scalar(),

        "projects":
            db.execute(
                text(
                    "SELECT COUNT(*) FROM Project"
                )
            ).scalar(),

        "approvals":
            db.execute(
                text(
                    "SELECT COUNT(*) FROM Approval"
                )
            ).scalar()
    }