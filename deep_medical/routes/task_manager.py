from fastapi import APIRouter, status
from uuid import UUID
from typing import Optional

from deep_medical.schemas.task_manager import (
    TaskManagerSchema,
    NewTaskManagerSchema,
    TaskManagerPatchSchema
)
from deep_medical.actions.task_manager import (
    create_new_task, get_all_tasks,
    get_task_by_id,
    delete_task_by_id,
    update_task_by_id,
    patch_task_by_id
)

task_router = APIRouter()


@task_router.post('/tasks', status_code=status.HTTP_201_CREATED)
async def create_tasks(task: NewTaskManagerSchema) -> TaskManagerSchema:
    """Creates a new task."""
    result = await create_new_task(task)
    return result


@task_router.get('/tasks', status_code=status.HTTP_200_OK)
async def get_tasks(
    completed: Optional[bool] = None
) -> list[TaskManagerSchema]:
    """Gets all tasks.
    Filter available by fetching all tasks based on the completed status
    """
    results = await get_all_tasks(completed=completed)
    return results


@task_router.get('/tasks/{id}', status_code=status.HTTP_200_OK)
async def get_task_from_id(id: UUID) -> TaskManagerSchema:
    """Get a single task by its ID. Raises 404 if not found."""
    result = await get_task_by_id(id)
    return result


@task_router.put('/tasks/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_task(id: UUID, task: NewTaskManagerSchema) -> None:
    """Update a single task by its ID.
    Raises 404 if the ID of the task to be updated is not found.
    """
    await update_task_by_id(id, task)
    return


@task_router.delete('/tasks/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: UUID) -> None:
    """Delete a task by ID.
    Raises 404 if the ID of the task to be deleted is not found.
    """
    await delete_task_by_id(id)
    return


@task_router.patch('/tasks/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def patch_task(id: UUID, task: TaskManagerPatchSchema) -> None:
    """Partially update a tast.
    Raises 404 if the ID of the task to be patched is not found.
    """
    await patch_task_by_id(id, task)
    return