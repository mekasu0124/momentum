from sqlalchemy import (
    Column,
    UUID,
    DateTime,
    String,
    Text
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
        unique = True,
        default = lambda: uuid4()
    )

    title = Column(
        String(75),
        index = True,
        unique = True
    )

    content = Column(Text(255))

    created_at = Column(
        DateTime,
        index = True,
        default = lambda: datetime.now()
    )

    def __repr__(self):
        return f"ID: {self.id}\nTitle: {self.title}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at
        }