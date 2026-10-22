import uuid
from datetime import datetime, timezone

from fastapi import HTTPException

from app.models.entities import Approval


class ApprovalService:

    def approve(
        self,
        db,
        approval_id,
        approved_by
    ):

        row = db.get(
            Approval,
            approval_id
        )

        if not row:
            raise HTTPException(
                404,
                "Approval not found"
            )

        row.Status = "Approved"
        row.DecisionAtUtc = datetime.now(
            timezone.utc
        )

        row.Comments = approved_by

        db.commit()

        return row

    def reject(
        self,
        db,
        approval_id,
        comments
    ):

        row = db.get(
            Approval,
            approval_id
        )

        if not row:
            raise HTTPException(
                404,
                "Approval not found"
            )

        row.Status = "Rejected"
        row.Comments = comments

        db.commit()

        return row

    def request_information(
        self,
        db,
        approval_id,
        comments
    ):

        row = db.get(
            Approval,
            approval_id
        )

        if not row:
            raise HTTPException(
                404,
                "Approval not found"
            )

        row.Status = "InformationRequired"
        row.Comments = comments

        db.commit()

        return row