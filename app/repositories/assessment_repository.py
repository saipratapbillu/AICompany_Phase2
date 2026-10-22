import json, uuid
from datetime import datetime, timezone
from sqlalchemy import text, select, func
from app.models.entities import RequirementAssessment
class AssessmentRepository:
    def next_version(self,db,requirement_id): return (db.execute(select(func.max(RequirementAssessment.AssessmentVersion)).where(RequirementAssessment.RequirementID==requirement_id)).scalar() or 0)+1
    def create(self,db,requirement,ceo,correlation_id,version,result,requested_by):
        row=RequirementAssessment(RequirementAssessmentID=uuid.uuid4(),RequirementID=requirement.RequirementID,AssessedByAgentID=ceo.AgentID,CorrelationID=correlation_id,AssessmentVersion=version,Classification=result.classification,BusinessDomain=result.business_domain,Complexity=result.complexity,RiskLevel=result.risk_level,Feasibility=result.feasibility,FeasibilityScore=result.feasibility_score,ConfidenceScore=result.confidence_score,ExecutiveSummary=result.executive_summary,AssumptionsJson=json.dumps(result.assumptions),ConstraintsJson=json.dumps(result.constraints),RisksJson=json.dumps([x.model_dump() for x in result.risks]),AssessmentJson=result.model_dump_json(),HumanApprovalRequired=result.human_approval_required,AssessmentStatus="Completed",Model=ceo.Model,ModelVersion=ceo.ModelVersion,PromptVersion=ceo.PromptVersion,CreatedAtUtc=datetime.now(timezone.utc),CreatedBy=requested_by)
        db.add(row); db.flush()
        for d in result.departments:
            db.execute(text("""INSERT INTO RequirementAssessmentDepartment(RequirementAssessmentID,DepartmentID,Responsibility,IsLeadDepartment,Priority,Status) SELECT :aid,DepartmentID,:resp,:lead,:priority,'Proposed' FROM Department WHERE DepartmentName=:name"""),{"aid":row.RequirementAssessmentID,"resp":d.responsibility,"lead":d.is_lead_department,"priority":d.priority,"name":d.department_name})
        for s in result.required_skills:
            db.execute(text("""IF NOT EXISTS(SELECT 1 FROM RequirementSkill rs JOIN Skill sk ON sk.SkillID=rs.SkillID WHERE rs.RequirementID=:rid AND sk.Name=:name) INSERT INTO RequirementSkill(RequirementID,SkillID,Priority,MinimumProficiency,SkillPurpose,EstimatedEffortHours,IsMandatory) SELECT :rid,SkillID,:priority,:prof,:purpose,:hours,:mandatory FROM Skill WHERE Name=:name"""),{"rid":requirement.RequirementID,"name":s.skill_name,"priority":s.priority,"prof":s.minimum_proficiency,"purpose":s.purpose,"hours":s.estimated_effort_hours,"mandatory":s.is_mandatory})
        return row
