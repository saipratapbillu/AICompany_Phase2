import uuid
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import Requirement
from app.schemas.schemas import AssessmentRequest, AssessmentResponse, RequirementCreate, RequirementUpdate
from app.repositories.requirement_repository import RequirementRepository
from app.repositories.agent_repository import AgentRepository
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.audit_repository import AuditRepository
from app.services.assessment_provider import DeterministicAssessmentProvider
from app.services.policy_service import PolicyService
from app.services.ceo_orchestrator import CEOOrchestrator

router = APIRouter(prefix="/requirements", tags=["Requirements"])


def service():
    return CEOOrchestrator(
        RequirementRepository(), AgentRepository(), AssessmentRepository(),
        AuditRepository(), DeterministicAssessmentProvider(), PolicyService()
    )


def serialize_requirement(item: Requirement):
    return {
        "requirement_id": str(item.RequirementID),
        "title": item.Title,
        "description": item.Description,
        "requested_by": item.RequestedBy,
        "priority": item.Priority,
        "risk_level": item.RiskLevel,
        "status": item.Status,
        "created_at_utc": item.CreatedAtUtc,
        "created_by": item.CreatedBy,
        "modified_at_utc": item.ModifiedAtUtc,
        "modified_by": item.ModifiedBy,
    }


@router.get("")
def list_requirements(db: Session = Depends(get_db)):
    rows = db.execute(
        select(Requirement).order_by(Requirement.CreatedAtUtc.desc())
    ).scalars().all()
    return [serialize_requirement(row) for row in rows]


@router.get("/{requirement_id}")
def get_requirement(requirement_id: UUID, db: Session = Depends(get_db)):
    item = db.get(Requirement, requirement_id)
    if not item:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return serialize_requirement(item)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_requirement(body: RequirementCreate, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    item = Requirement(
        RequirementID=uuid.uuid4(),
        Title=body.title.strip(),
        Description=body.description.strip(),
        RequestedBy=body.requested_by.strip(),
        Priority=body.priority,
        RiskLevel="Low",
        Status="Submitted",
        CreatedAtUtc=now,
        CreatedBy=body.requested_by.strip(),
        ModifiedAtUtc=now,
        ModifiedBy=body.requested_by.strip(),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return serialize_requirement(item)


@router.put("/{requirement_id}")
def update_requirement(
    requirement_id: UUID,
    body: RequirementUpdate,
    db: Session = Depends(get_db),
):
    item = db.get(Requirement, requirement_id)
    if not item:
        raise HTTPException(status_code=404, detail="Requirement not found")
    if item.Status not in {"Submitted", "Assessed", "AssessmentFailed", "InformationRequired"}:
        raise HTTPException(
            status_code=409,
            detail=f"Requirement cannot be edited while status is {item.Status}",
        )
    changes = body.model_dump(exclude_unset=True)
    field_map = {
        "title": "Title", "description": "Description", "requested_by": "RequestedBy",
        "priority": "Priority"
    }
    for source, target in field_map.items():
        if source in changes:
            value = changes[source]
            setattr(item, target, value.strip() if isinstance(value, str) else value)
    item.ModifiedAtUtc = datetime.now(timezone.utc)
    item.ModifiedBy = body.modified_by.strip()
    db.commit()
    db.refresh(item)
    return serialize_requirement(item)


@router.post("/{requirement_id}/assess", response_model=AssessmentResponse)
def assess_requirement(
    requirement_id: UUID,
    body: AssessmentRequest,
    db: Session = Depends(get_db),
):
    row, result = service().assess(
        db, requirement_id, body.requested_by, body.force_reassessment
    )
    return AssessmentResponse(
        requirement_id=requirement_id,
        assessment_id=row.RequirementAssessmentID,
        correlation_id=row.CorrelationID,
        status="Assessed",
        assessment=result,
    )
