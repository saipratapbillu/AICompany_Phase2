import uuid
from sqlalchemy import (
    String,
    Text,
    Integer,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.dialects.mssql import ( UNIQUEIDENTIFIER)
from sqlalchemy.orm import ( Mapped, mapped_column, relationship)
from app.db.session import Base

class Requirement(Base):
    __tablename__="Requirement"
    RequirementID:Mapped[uuid.UUID]=mapped_column(UNIQUEIDENTIFIER,primary_key=True)
    Title:Mapped[str]=mapped_column(String(200)); Description:Mapped[str]=mapped_column(Text)
    RequestedBy:Mapped[str]=mapped_column(String(200)); Priority:Mapped[str]=mapped_column(String(20))
    RiskLevel:Mapped[str]=mapped_column(String(20)); Status:Mapped[str]=mapped_column(String(30))
    CreatedAtUtc:Mapped[object]=mapped_column(DateTime); CreatedBy:Mapped[str]=mapped_column(String(200))
    ModifiedAtUtc:Mapped[object]=mapped_column(DateTime); ModifiedBy:Mapped[str]=mapped_column(String(200))

class Agent(Base):
    __tablename__="Agent"
    AgentID:Mapped[uuid.UUID]=mapped_column(UNIQUEIDENTIFIER,primary_key=True)
    AgentName:Mapped[str]=mapped_column(String(200)); AgentType:Mapped[str]=mapped_column(String(30)); Status:Mapped[str]=mapped_column(String(30))
    CompanyID:Mapped[uuid.UUID]=mapped_column(UNIQUEIDENTIFIER); Model:Mapped[str|None]=mapped_column(String(100)); ModelVersion:Mapped[str|None]=mapped_column(String(50)); PromptVersion:Mapped[str|None]=mapped_column(String(50))

class RequirementAssessment(Base):
    __tablename__="RequirementAssessment"
    RequirementAssessmentID:Mapped[uuid.UUID]=mapped_column(UNIQUEIDENTIFIER,primary_key=True,default=uuid.uuid4)
    RequirementID:Mapped[uuid.UUID]=mapped_column(UNIQUEIDENTIFIER,ForeignKey("Requirement.RequirementID"))
    AssessedByAgentID:Mapped[uuid.UUID]=mapped_column(UNIQUEIDENTIFIER,ForeignKey("Agent.AgentID"))
    CorrelationID:Mapped[uuid.UUID]=mapped_column(UNIQUEIDENTIFIER); AssessmentVersion:Mapped[int]=mapped_column(Integer)
    Classification:Mapped[str]=mapped_column(String(100)); BusinessDomain:Mapped[str|None]=mapped_column(String(150))
    Complexity:Mapped[str]=mapped_column(String(20)); RiskLevel:Mapped[str]=mapped_column(String(20)); Feasibility:Mapped[str]=mapped_column(String(30))
    FeasibilityScore:Mapped[float|None]=mapped_column(Numeric(5,2)); ConfidenceScore:Mapped[float|None]=mapped_column(Numeric(5,2))
    ExecutiveSummary:Mapped[str]=mapped_column(String(2000)); AssumptionsJson:Mapped[str|None]=mapped_column(Text); ConstraintsJson:Mapped[str|None]=mapped_column(Text); RisksJson:Mapped[str|None]=mapped_column(Text); AssessmentJson:Mapped[str]=mapped_column(Text)
    HumanApprovalRequired:Mapped[bool]=mapped_column(Boolean); AssessmentStatus:Mapped[str]=mapped_column(String(30)); Model:Mapped[str|None]=mapped_column(String(100)); ModelVersion:Mapped[str|None]=mapped_column(String(50)); PromptVersion:Mapped[str|None]=mapped_column(String(50)); CreatedAtUtc:Mapped[object]=mapped_column(DateTime); CreatedBy:Mapped[str]=mapped_column(String(200))

class Role(Base):
    __tablename__ = "Role"

    RoleID: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4
    )
    RoleCode: Mapped[str] = mapped_column(String(50))
    RoleName: Mapped[str] = mapped_column(String(100))
    RoleLevel: Mapped[int] = mapped_column(Integer)
    IsActive: Mapped[bool] = mapped_column(Boolean,default=True)

class AppUser(Base):
    __tablename__ = "AppUser"

    UserID: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4
    )
    Email: Mapped[str] = mapped_column(String(255))
    PasswordHash: Mapped[str] = mapped_column(String(500))
    DisplayName: Mapped[str] = mapped_column(String(200))
    Department: Mapped[str | None] = mapped_column(String(100))
    RoleID: Mapped[uuid.UUID | None] = mapped_column(UNIQUEIDENTIFIER, ForeignKey("Role.RoleID"))
    IsActive: Mapped[bool] = mapped_column(Boolean,default=True)
    Role = relationship("Role")

class Approval(Base):
    __tablename__ = "Approval"

    ApprovalID: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4
    )

    RequirementID: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        ForeignKey("Requirement.RequirementID")
    )

    AssignedToUserID: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        ForeignKey("AppUser.UserID")
    )

    ApprovalLevel: Mapped[int] = mapped_column(Integer)
    Status: Mapped[str] = mapped_column(String(30))
    Comments: Mapped[str | None] = mapped_column(Text)
    CreatedAtUtc: Mapped[object] = mapped_column(DateTime)
    DecisionAtUtc: Mapped[object | None] = mapped_column(DateTime)

class Project(Base):
    __tablename__ = "Project"

    ProjectID: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4
    )

    RequirementID: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        ForeignKey("Requirement.RequirementID")
    )

    ProjectName: Mapped[str] = mapped_column(String(300))
    Status: Mapped[str] = mapped_column(String(30))
    CreatedAtUtc: Mapped[object] = mapped_column(DateTime)

