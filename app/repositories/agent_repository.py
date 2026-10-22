from sqlalchemy import select
from app.models.entities import Agent
class AgentRepository:
    def get_active_ceo(self,db): return db.execute(select(Agent).where(Agent.AgentName=="AI CEO",Agent.AgentType=="Executive",Agent.Status=="Active")).scalar_one_or_none()
