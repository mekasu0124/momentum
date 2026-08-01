from sqlalchemy import (
    Column,
    UUID,
    DateTime,
    String
)
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

from ..database.db import get_base


Base = get_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        default=lambda: uuid4()
    )

    email = Column(
        String(255),
        index=True,
        unique=True,
        nullable=False
    )

    username = Column(
        String(50),
        index=True,
        unique=True,
        nullable=False
    )

    hashed_password = Column(String(255), nullable=False)

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

    # Relationships
    tasks = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    graveyard_tasks = relationship(
        "TaskGraveyard",
        back_populates="user",
        cascade="all, delete-orphan"
    )
