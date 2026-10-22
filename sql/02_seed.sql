USE AICompany;
GO
DECLARE @Company uniqueidentifier=NEWID();
INSERT INTO Company(CompanyID,CompanyName) VALUES(@Company,'Local AI Company');
DECLARE @Departments TABLE(Name nvarchar(150));
INSERT INTO @Departments VALUES ('Executive'),('Finance'),('HR'),('Procurement'),('PMO'),('Technology'),('Data & Analytics'),('Cybersecurity'),('Operations'),('Warehouse'),('Sales'),('Marketing'),('Legal & Compliance'),('Risk'),('Quality'),('Internal Audit');
INSERT INTO Department(CompanyID,DepartmentName) SELECT @Company,Name FROM @Departments;
DECLARE @Exec uniqueidentifier=(SELECT DepartmentID FROM Department WHERE CompanyID=@Company AND DepartmentName='Executive');
DECLARE @Pos uniqueidentifier=NEWID(); INSERT INTO Position(PositionID,DepartmentID,PositionName,Grade) VALUES(@Pos,@Exec,'CEO Agent','Executive');
INSERT INTO Agent(AgentID,CompanyID,DepartmentID,PositionID,AgentName,AgentType,Grade,JobDescription,ResponsibilitiesJson,Model,ModelVersion,PromptVersion,AutonomyLevel,RiskLevel,CostLimitMonthly,TokenLimitDaily,ConcurrentTaskLimit,Status,CreatedBy,ModifiedBy)
VALUES(NEWID(),@Company,@Exec,@Pos,'AI CEO','Executive','Executive','Executive orchestration only','["Requirement intake","Delegation","Portfolio monitoring","Escalation"]','UNCONFIGURED','UNCONFIGURED','1.0.0',2,'High',1000,100000,10,'Active','bootstrap','bootstrap');
INSERT INTO Skill(Name,Description,Version,RiskLevel,Owner,Status) VALUES
('RequirementAnalysis','Interpret and structure business requirements','1.0.0','Low','Enterprise Architecture','Approved'),
('ProjectPlanning','Create governed project plans','1.0.0','Medium','PMO','Approved'),
('SQLDevelopment','Develop database objects in sandbox','1.0.0','Medium','Data & Analytics','Approved'),
('PowerBIDevelopment','Build governed BI assets','1.0.0','Medium','Data & Analytics','Approved'),
('SecurityReview','Review security architecture and evidence','1.0.0','High','Cybersecurity','Approved');
GO
