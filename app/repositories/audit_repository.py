import json
from sqlalchemy import text
class AuditRepository:
    def write(self,db,correlation_id,actor_type,actor_id,action,resource_type,resource_id,outcome,details=None):
        db.execute(text("""INSERT INTO AuditLog(CorrelationID,ActorType,ActorID,Action,ResourceType,ResourceID,Outcome,Details) VALUES(:c,:at,:ai,:a,:rt,:ri,:o,:d)"""),{"c":correlation_id,"at":actor_type,"ai":actor_id,"a":action,"rt":resource_type,"ri":resource_id,"o":outcome,"d":json.dumps(details or {})})
