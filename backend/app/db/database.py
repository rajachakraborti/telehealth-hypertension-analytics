from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use absolute path so the DB file is always in the backend directory
# regardless of where uvicorn is launched from
_DB_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DB_PATH = os.path.join(_DB_DIR, "telehealth.db")

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{_DB_PATH}"
)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()