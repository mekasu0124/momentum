from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    task: str


class TaskUpdate(BaseModel):
    task: Optional[str] = None
    is_completed: Optional[bool] = None

    model_config = ConfigDict(
        from_attributes = True
    )

class TaskResponse(BaseModel):
    id: str
    task: str
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes = True
    )