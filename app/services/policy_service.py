class PolicyService:
    def apply(self,requirement,result):
        if result.complexity in {'High','Critical'} or requirement.Priority=='Critical': result.human_approval_required=True
        if result.risk_level=='Low' and any(x in requirement.Description.lower() for x in ['security','personal data','employee','payment']): result.risk_level='Medium'
        return result
