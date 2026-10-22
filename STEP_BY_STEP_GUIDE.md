# AI Company Phase 2: Complete Setup and User Guide

This guide is for both technical administrators and first-time business users. The project runs locally with FastAPI, SQL Server, SQLAlchemy, ODBC Driver 17, and a browser-based requirement workspace.

## 1. What this version includes

- Health check and SQL Server connectivity
- AI Agent registry listing
- Friendly browser UI at `http://127.0.0.1:8000/`
- Create, list, view and update requirements
- Send an existing requirement to the AI CEO for structured assessment
- Persist assessment evidence, involved departments and required skills
- Audit lifecycle actions using a Correlation ID
- Swagger API documentation at `http://127.0.0.1:8000/docs`

## 2. Prerequisites

Install these before starting:

1. Windows 10 or Windows 11
2. SQL Server Developer Edition or an accessible local SQL Server instance
3. SQL Server Management Studio
4. Python 3.11 or newer
5. Microsoft ODBC Driver 17 for SQL Server

Confirm Python:

```cmd
python --version
```

Confirm the available ODBC driver:

```cmd
python -c "import pyodbc; print(pyodbc.drivers())"
```

The result must include:

```text
ODBC Driver 17 for SQL Server
```

## 3. Extract the project

Extract the ZIP to a short local path, for example:

```text
C:\AICompany\AI_Company_Phase2_UI
```

Avoid running directly from inside the ZIP.

## 4. Prepare the SQL Server database

If the original `AICompany` database and base tables already exist, run only:

```text
sql\03_phase2_assessment.sql
```

This adds the Phase 2 assessment tables without deleting existing requirements.

If starting from a completely new environment, first run the original base scripts:

1. `01_create_database.sql`
2. `01_seed.sql`
3. `sql\03_phase2_assessment.sql`

After the migration, verify:

```sql
USE AICompany;
GO

SELECT name
FROM sys.tables
WHERE name IN
(
    'Requirement',
    'RequirementAssessment',
    'RequirementAssessmentDepartment',
    'RequirementSkill',
    'AuditLog'
);
```

## 5. Configure the application

Copy `.env.example` and rename the copy to `.env`.

Default configuration:

```env
DATABASE_URL=mssql+pyodbc://@localhost/AICompany?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes
```

If SQL Server uses a named instance, replace `localhost` with the exact instance. Example:

```env
DATABASE_URL=mssql+pyodbc://@localhost\SQLEXPRESS/AICompany?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes
```

## 6. Create the Python environment

Open Command Prompt inside the project folder:

```cmd
cd C:\AICompany\AI_Company_Phase2_UI
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 7. Start the application

Run:

```cmd
run_local.bat
```

Keep the command window open. It contains useful error details.

Open:

- User interface: `http://127.0.0.1:8000/`
- Swagger API: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

Expected health response:

```json
{
  "status": "ok",
  "database": "AICompany",
  "server": "localhost"
}
```

## 8. How a new user creates a requirement

1. Open the user interface.
2. Enter a clear requirement title.
3. Describe the business problem and expected outcome.
4. Mention systems such as SharePoint, SQL Server or Power BI when required.
5. Enter the requester name.
6. Select Low, Medium, High or Critical priority.
7. Select **Submit requirement**.
8. The new card appears in the Requirements list.

Recommended description structure:

```text
Business problem:
Expected outcome:
Users or departments:
Required systems:
Reports and dashboards:
Security and approvals:
Notifications and deadlines:
```

Example:

```text
Design and build a supplier compliance management platform. Use SharePoint for documents, SQL Server for structured data and Power BI for dashboards. Support certificate expiry, audit findings, corrective actions, role-based access, notifications and approval workflows.
```

## 9. How to view or update a requirement

1. Select a requirement card in the right-side list.
2. Review its title, priority, owner, risk, status and description.
3. Select **Edit**.
4. Update the form.
5. Select **Update requirement**.

Editing is allowed only for safe pre-execution statuses such as Submitted, Assessed, AssessmentFailed and InformationRequired.

## 10. How to request AI CEO assessment

1. Select a requirement.
2. Select **Send to AI CEO for assessment**.
3. Wait for the structured result.
4. Review classification, business domain, complexity, risk, feasibility, approval requirement and involved departments.

The current package uses a deterministic provider so it works without Azure OpenAI. The provider can later be replaced with a governed model integration.

## 11. What happens during assessment

1. API receives the requirement ID.
2. Control plane locks the requirement for assessment.
3. Active AI CEO is loaded from the Agent table.
4. A new Correlation ID is created.
5. Assessment provider creates structured output.
6. Pydantic validates the output.
7. Policy rules enforce approval and risk requirements.
8. Full evidence is inserted into `RequirementAssessment`.
9. Departments are inserted into `RequirementAssessmentDepartment`.
10. Skills are inserted into `RequirementSkill`.
11. Requirement risk and status are updated.
12. Lifecycle evidence is written to `AuditLog`.

## 12. Verify data in SQL Server

Latest requirements:

```sql
SELECT TOP 20 *
FROM dbo.Requirement
ORDER BY CreatedAtUtc DESC;
```

Latest assessments:

```sql
SELECT TOP 20 *
FROM dbo.RequirementAssessment
ORDER BY CreatedAtUtc DESC;
```

Departments selected for assessments:

```sql
SELECT
    ra.RequirementID,
    d.DepartmentName,
    rad.Responsibility,
    rad.IsLeadDepartment,
    rad.Priority,
    rad.Status
FROM dbo.RequirementAssessmentDepartment rad
JOIN dbo.RequirementAssessment ra
    ON ra.RequirementAssessmentID = rad.RequirementAssessmentID
JOIN dbo.Department d
    ON d.DepartmentID = rad.DepartmentID
ORDER BY ra.CreatedAtUtc DESC;
```

Required skills:

```sql
SELECT
    rs.RequirementID,
    s.Name AS SkillName,
    rs.Priority,
    rs.MinimumProficiency,
    rs.SkillPurpose,
    rs.EstimatedEffortHours,
    rs.IsMandatory
FROM dbo.RequirementSkill rs
JOIN dbo.Skill s
    ON s.SkillID = rs.SkillID;
```

Audit history:

```sql
SELECT TOP 100 *
FROM dbo.AuditLog
ORDER BY CreatedAtUtc DESC;
```

## 13. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Validate API and database connectivity |
| GET | `/agents` | List registered AI employees |
| GET | `/requirements` | List all requirements |
| GET | `/requirements/{id}` | Get one requirement |
| POST | `/requirements` | Create a requirement |
| PUT | `/requirements/{id}` | Update a requirement |
| POST | `/requirements/{id}/assess` | Run AI CEO assessment |

## 14. Troubleshooting

### Swagger works but health returns 500

Check the command-window traceback. Confirm the installed driver and `.env` connection string both use `ODBC Driver 17 for SQL Server`.

### Database login or server not found

Confirm the exact server name in SSMS. If it is `localhost\SQLEXPRESS`, use the same instance in `.env`.

### Assessment endpoint is missing

Stop and restart FastAPI after replacing the project files:

```cmd
Ctrl+C
run_local.bat
```

Refresh Swagger using `Ctrl+F5`.

### Requirement assessment returns a duplicate/version issue

Send `force_reassessment` as true. Each assessment uses a new version number.

### UI appears old after an update

Use `Ctrl+F5` or clear the browser cache.

## 15. Security and production warning

This is a local MVP. Before production, add Microsoft Entra workload identities, Azure Key Vault or another approved secret vault, environment-separated credentials, HTTPS, content security controls, API authorization, immutable audit storage, model evaluation gates, approval enforcement and restricted tool execution.

## 16. Recommended next phase

After this Phase 2 package is stable, implement:

1. Human approval API and UI
2. Project Factory
3. Task and dependency generation
4. Workforce Manager
5. Agent capacity and skill matching
6. Deliverable review and evaluation
7. Security approval gate
8. Deployment control
9. Knowledge capture and project closure
