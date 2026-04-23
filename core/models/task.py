from sqlalchemy import (
    Column,
    String,
    Integer
)

from ..database.db import get_base


Base = get_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(
        Integer,
        primary_key = True,
        index = True,
        autoincrement = True
    )

    content = Column(String)