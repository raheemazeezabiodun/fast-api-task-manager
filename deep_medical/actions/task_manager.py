from uuid import UUID
from typing import Optional

from deep_medical.schemas.task_manager import (
    NewTaskManagerSchema,
    TaskManagerSchema
)
from deep_medical.repos.task_manager import TaskManagerRepo
from deep_medical import exceptions as exc


async def create_new_task(payload: NewTaskManagerSchema) -> TaskManagerSchema:
    task = await TaskManagerRepo.save(payload)
    return task


async def get_all_tasks(completed: Optional[bool] = None) -> list[TaskManagerSchema]:
    tasks = await TaskManagerRepo.get_tasks(completed)
    return tasks


async def get_task_by_id(id: UUID) -> TaskManagerSchema:
    task = await TaskManagerRepo.get_task_from_id(id)
    if not task:
        raise exc.NotFoundException(f"Task not found for id={id}")
    return task


async def delete_task_by_id(id: UUID) -> None:
    task_id = await TaskManagerRepo.delete_task_from_id(id)
    if not task_id:
        raise exc.NotFoundException(f"Task not found for id={id}, cannot delete")
    return None


async def update_task_by_id(id: UUID, task: NewTaskManagerSchema) -> None:
    task_id = await TaskManagerRepo.update_task_by_id(id, task)
    if not task_id:
        raise exc.NotFoundException(f"Task not found for id={id}, cannot update")
    return None
