from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for creating a new user from the registration form."""
    email: str = Field(..., min_length=1, max_length=255, description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="User's chosen username")
    cr_password: str = Field(..., min_length=8, max_length=128, description="Created password")
    cf_password: str = Field(..., min_length=8, max_length=128, description="Confirmed password")

    @model_validator(mode='after')
    def validate_passwords_match(self):
        if self.cr_password != self.cf_password:
            raise ValueError("Passwords do not match")
        return self


class UserUpdate(BaseModel):
    email: Optional[str] = Field(None, min_length=1, max_length=255)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True