from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class TaskEnergy(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    completed = "completed"
    archived = "archived"

class TaskCategory(str, Enum):
    work = "work"
    personal = "personal"
    health = "health"
    learning = "learning"
    social = "social"
    other = "other"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    energy: TaskEnergy = TaskEnergy.medium
    category: TaskCategory = TaskCategory.other
    due_date: Optional[datetime] = None
    tags: List[str] = []

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    energy: Optional[TaskEnergy] = None
    status: Optional[TaskStatus] = None
    category: Optional[TaskCategory] = None
    due_date: Optional[datetime] = None
    focus_minutes: Optional[int] = None
    tags: Optional[List[str]] = None
    is_avoidance: Optional[bool] = None
    emotion_score: Optional[float] = None

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    energy: str
    status: str
    category: str
    created_at: float
    completed_at: Optional[float] = None
    due_date: Optional[float] = None
    focus_minutes: int = 0
    tags: List[str] = []
    is_avoidance: bool = False
    emotion_score: float = 0.0
    original_brain_dump: Optional[str] = None

    class Config:
        from_attributes = True 