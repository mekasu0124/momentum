from pydantic import BaseModel, Field
from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=75)
    content: str = Field(..., min_length=1, max_length=255)


class TaskUpdate:
    id: str
    title: str
    content: str
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class TaskResponse:
    id: str
    title: str
    content: str
    created_at: str
    updated_at: Optional[str]