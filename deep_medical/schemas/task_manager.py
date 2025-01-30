from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from deep_medical.models.task_manager import TaskManager


class TaskManagerSchema(BaseModel):
    id: UUID
    created_at: datetime
    title: str
    completed: bool
    description: Optional[str] = None

    @classmethod
    def from_entity(cls, entity: TaskManager) -> "TaskManagerSchema":
        return cls(**entity.model_dump())


class NewTaskManagerSchema(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False


class TaskManagerPatchSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
