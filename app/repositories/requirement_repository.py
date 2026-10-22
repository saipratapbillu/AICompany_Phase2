from sqlalchemy import select
from app.models.entities import Requirement
class RequirementRepository:
    def get(self,db,requirement_id): return db.get(Requirement,requirement_id)
    def get_for_update(self,db,requirement_id): return db.execute(select(Requirement).where(Requirement.RequirementID==requirement_id).with_for_update()).scalar_one_or_none()
