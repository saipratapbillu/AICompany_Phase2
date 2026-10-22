import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL", "mssql+pyodbc://@localhost/AICompany?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes")
engine=create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal=sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
class Base(DeclarativeBase): pass
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
