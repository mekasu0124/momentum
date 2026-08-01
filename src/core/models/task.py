from sqlalchemy import (
    Column,
    UUID,
    String,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

from ..database.db import get_base


Base = get_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        default=lambda: uuid4()
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    title = Column(
        String(75),
        index=True,
        unique=True,
        nullable=False
    )

    content = Column(
        Text(255),
        index=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        index=True,
        nullable=False,
        default=lambda: datetime.now()
    )

    updated_at = Column(
        DateTime,
        index=True,
        nullable=True,
        onupdate=lambda: datetime.now()
    )

    # Relationship
    user = relationship("User", back_populates="tasks")
