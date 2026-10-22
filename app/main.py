from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.approvals import router as approvals_router
from app.api.projects import router as projects_router

from app.api.requirements import router as requirements_router
from app.db.session import get_db

from app.api.dashboard import router as dashboard_router

app = FastAPI(title="AI Company Phase 2", version="2.1.0")
app.include_router(requirements_router)

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def ui():
    return FileResponse(STATIC_DIR / "landing.html")


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "AICompany", "server": "localhost"}


@app.get("/agents")
def agents(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT AgentID, AgentName, AgentType, Grade, AutonomyLevel,
               RiskLevel, Status, CurrentWorkload
        FROM Agent ORDER BY AgentName
    """)).mappings().all()
    return [dict(row) for row in rows]


app = FastAPI(
    title="AI Workforce OS",
    version="3.0.0"
)

STATIC_DIR = Path(__file__).resolve().parent / "static"

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

app.include_router(requirements_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(approvals_router)
app.include_router(projects_router)
app.include_router(dashboard_router)

@app.get("/", include_in_schema=False)
def ui():
    return FileResponse(
        STATIC_DIR / "landing.html"
    )

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "ok"
    }

@app.get("/login", include_in_schema=False)
def login_page():
    return FileResponse(
        STATIC_DIR / "login.html"
    )

@app.get("/register", include_in_schema=False)
def register_page():
    return FileResponse(
        STATIC_DIR / "register.html"
    )

@app.get("/profile", include_in_schema=False)
def profile_page():
    return FileResponse(
        STATIC_DIR / "profile.html"
    )

@app.get("/dashboard", include_in_schema=False)
def dashboard_page():
    return FileResponse(
        STATIC_DIR / "dashboard.html"
    )