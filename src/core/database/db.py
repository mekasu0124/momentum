from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ...config import Config

app_dir = Config.APP_DIR
db_path = app_dir / "main.db"

SQL_DB_URL = f"sqlite:///{db_path}"

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
