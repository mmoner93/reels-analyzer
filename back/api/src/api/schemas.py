from pydantic import BaseModel, ConfigDict
from datetime import datetime
from api.models import TaskStatus


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
