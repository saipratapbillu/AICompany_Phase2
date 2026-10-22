class DeterministicAssessmentProvider:
    def assess(self,requirement):
        text=(requirement.Title+' '+requirement.Description).lower()
        deps=[{"department_name":"PMO","responsibility":"Govern planning, dependencies and delivery.","is_lead_department":True,"priority":"High"}]
        mapping={"Procurement":["supplier","vendor","procurement"],"Data & Analytics":["sql","power bi","analytics","dashboard"],"Technology":["system","platform","api","sharepoint"],"Cybersecurity":["security","role-based"],"Legal & Compliance":["compliance"],"Quality":["quality","audit"]}
        for name,words in mapping.items():
            if any(w in text for w in words): deps.append({"department_name":name,"responsibility":f"Provide {name} governance and delivery support.","is_lead_department":False,"priority":"High" if name in ['Procurement','Technology','Data & Analytics'] else "Medium"})
        skills=[]
        for name,purpose,hours in [("RequirementAnalysis","Structure business requirements",40),("ProjectPlanning","Create governed delivery plan",24),("SQLDevelopment","Implement SQL data layer",80),("PowerBIDevelopment","Create dashboards",60),("SecurityReview","Review security controls",24)]: skills.append({"skill_name":name,"priority":"High","minimum_proficiency":4,"purpose":purpose,"estimated_effort_hours":hours,"is_mandatory":True})
        return {"classification":"Enterprise Business Application","business_domain":"Supplier Compliance","complexity":"High","risk_level":"Medium","feasibility":"FeasibleWithConditions","feasibility_score":85,"confidence_score":90,"executive_summary":"The requirement is feasible using SharePoint, SQL Server and Power BI with governed approvals.","departments":deps,"required_skills":skills,"risks":[{"title":"Supplier document quality","risk_level":"Medium","description":"Documents may be missing, expired or inconsistent.","mitigation":"Use validation, expiry monitoring and approval controls."}],"assumptions":["Required platform connectivity is available."],"constraints":["Production deployment requires approval."],"human_approval_required":True}

from abc import ABC
from abc import abstractmethod


class AssessmentProvider(
    ABC
):

    @abstractmethod
    def assess(
        self,
        requirement
    ):
        pass
