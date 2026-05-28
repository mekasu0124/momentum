from sqlalchemy import (
    Column,
    DateTime,
    UUID,
    String,
    Boolean
)

from datetime import datetime
from uuid import uuid4

from ..database.db import get_base


Base = get_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(
        UUID(as_uuid=True),
        primary_key = True,
        index = True,
        default = lambda: uuid4()
    )

    task = Column(
        String,
        unique = True,
        index = True
    )

    is_completed = Column(
        Boolean,
        index = True,
        default = False
    )

    created_at = Column(
        DateTime,
        index = True,
        default = lambda: datetime.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "task": self.task,
            "is_completed": self.is_completed,
            "created_at": self.created_at
        }