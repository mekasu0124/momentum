from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

from ..config import Config

Base = declarative_base()

def get_sql_db_url():
    """Get SQLite database URL dynamically"""
    return Config.get_sqlite_url()

def get_connect_args():
    """Get connection arguments dynamically"""
    url = get_sql_db_url()
    if url.startswith('sqlite'):
        return {"check_same_thread": False}
    return {}

def get_engine():
    """Create engine dynamically to respect runtime Config changes"""
    return create_engine(
        url=get_sql_db_url(),
        echo=False,
        connect_args=get_connect_args()
    )

def get_session_local():
    """Create sessionmaker dynamically"""
    return sessionmaker(
        bind=get_engine(),
        autocommit=False,
        autoflush=False
    )

def get_base():
    return Base

@contextmanager
def get_db():
    """
    Context Manager for database sessions with 
    automatic rollback/close
    """
    SessionLocal = get_session_local()
    db = SessionLocal()
    
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()