from datetime import datetime
from enum import Enum

from sqlalchemy import Column, String, DateTime, Text, Integer
from api.database import Base


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    status = Column(String, default=TaskStatus.PENDING)
    transcript = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    language = Column(String, nullable=True)
    topics = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
