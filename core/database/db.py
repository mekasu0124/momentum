from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from pathlib import Path

from ..config import Config

SQL_DB_URL = Config.get_sqlite_url()

connect_args = {}
if SQL_DB_URL.startswith('sqlite'):
    connect_args = {"check_same_thread": False}

Base = declarative_base()

engine = create_engine(
    url=SQL_DB_URL,
    echo=False,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

def get_base():
    return Base

def get_engine():
    return engine

@contextmanager
def get_db():
    """
    Context Manager for database sessions with 
    automatic rollback/close
    """

    db = SessionLocal()

    try:
        yield db

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()