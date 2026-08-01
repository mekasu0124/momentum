from pydantic import BaseModel, Field
from typing import Optional


class TaskGraveyardCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=75)
    content: str = Field(..., min_length=1, max_length=255)


class TaskGraveyardResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class TaskGraveyardRestore(BaseModel):
    id: str
    title: str
    content: str
    created_at: str
    updated_at: Optional[str]