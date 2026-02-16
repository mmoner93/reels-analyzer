from pydantic import BaseModel, ConfigDict
from datetime import datetime
from api.models import TaskStatus


# User schemas
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# Task schemas
class TaskCreate(BaseModel):
    url: str


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    url: str
    status: TaskStatus
    transcript: str | None = None
    error_message: str | None = None
    language: str | None = None
    topics: str | None = None
    created_at: datetime
    updated_at: datetime
    user_id: int | None = None
