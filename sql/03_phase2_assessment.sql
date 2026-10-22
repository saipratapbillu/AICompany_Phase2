USE AICompany;
GO
IF OBJECT_ID('dbo.RequirementAssessment','U') IS NULL
CREATE TABLE dbo.RequirementAssessment(RequirementAssessmentID uniqueidentifier NOT NULL PRIMARY KEY DEFAULT NEWID(),RequirementID uniqueidentifier NOT NULL REFERENCES dbo.Requirement(RequirementID),AssessedByAgentID uniqueidentifier NOT NULL REFERENCES dbo.Agent(AgentID),CorrelationID uniqueidentifier NOT NULL,AssessmentVersion int NOT NULL DEFAULT 1,Classification nvarchar(100) NOT NULL,BusinessDomain nvarchar(150),Complexity varchar(20) NOT NULL,RiskLevel varchar(20) NOT NULL,Feasibility varchar(30) NOT NULL,FeasibilityScore decimal(5,2),ConfidenceScore decimal(5,2),ExecutiveSummary nvarchar(2000) NOT NULL,AssumptionsJson nvarchar(max),ConstraintsJson nvarchar(max),RisksJson nvarchar(max),AssessmentJson nvarchar(max) NOT NULL,HumanApprovalRequired bit NOT NULL DEFAULT 0,AssessmentStatus varchar(30) NOT NULL DEFAULT 'Completed',Model nvarchar(100),ModelVersion nvarchar(50),PromptVersion nvarchar(50),CreatedAtUtc datetime2 NOT NULL DEFAULT SYSUTCDATETIME(),CreatedBy nvarchar(200) NOT NULL,CONSTRAINT UQ_RequirementAssessment_Version UNIQUE(RequirementID,AssessmentVersion));
GO
IF OBJECT_ID('dbo.RequirementAssessmentDepartment','U') IS NULL
CREATE TABLE dbo.RequirementAssessmentDepartment(RequirementAssessmentID uniqueidentifier NOT NULL REFERENCES dbo.RequirementAssessment(RequirementAssessmentID),DepartmentID uniqueidentifier NOT NULL REFERENCES dbo.Department(DepartmentID),Responsibility nvarchar(1000) NOT NULL,IsLeadDepartment bit NOT NULL DEFAULT 0,Priority varchar(20) NOT NULL DEFAULT 'Medium',Status varchar(20) NOT NULL DEFAULT 'Proposed',PRIMARY KEY(RequirementAssessmentID,DepartmentID));
GO
IF COL_LENGTH('dbo.RequirementSkill','MinimumProficiency') IS NULL ALTER TABLE dbo.RequirementSkill ADD MinimumProficiency tinyint NULL;
IF COL_LENGTH('dbo.RequirementSkill','SkillPurpose') IS NULL ALTER TABLE dbo.RequirementSkill ADD SkillPurpose nvarchar(1000) NULL;
IF COL_LENGTH('dbo.RequirementSkill','EstimatedEffortHours') IS NULL ALTER TABLE dbo.RequirementSkill ADD EstimatedEffortHours decimal(10,2) NULL;
IF COL_LENGTH('dbo.RequirementSkill','IsMandatory') IS NULL ALTER TABLE dbo.RequirementSkill ADD IsMandatory bit NOT NULL CONSTRAINT DF_RequirementSkill_IsMandatory DEFAULT 1;
GO
IF NOT EXISTS(SELECT 1 FROM sys.indexes WHERE name='IX_RequirementAssessment_Correlation') CREATE INDEX IX_RequirementAssessment_Correlation ON dbo.RequirementAssessment(CorrelationID,CreatedAtUtc);
GO
