from typing import TypeAlias
from typing import Optional
from typing import Sequence
from uuid import UUID

from sqlalchemy import select, delete, update

from deep_medical.models.task_manager import TaskManager
from deep_medical.database import db_session
from deep_medical.schemas.task_manager import (
    NewTaskManagerSchema,
    TaskManagerSchema
)


class TaskManagerRepo:
    model: TypeAlias = TaskManager

    @classmethod
    async def save(cls, task: NewTaskManagerSchema) -> TaskManagerSchema:
        data = cls.model(**task.model_dump())
        async with db_session() as session:
            session.add(data)
            await session.commit()
            await session.refresh(data)
            return TaskManagerSchema.from_entity(data)

    @classmethod
    async def get_tasks(cls, completed: Optional[bool] = None) -> list[TaskManagerSchema]:
        query = select(cls.model)
        if completed is not None:
            query = query.where(cls.model.completed == completed)
        async with db_session() as session:
            result = await session.execute(query)
            entities: Sequence[TaskManager] = result.scalars().all()
            return list(map(TaskManagerSchema.from_entity, entities))

    @classmethod
    async def get_task_from_id(cls, id: UUID) -> Optional[TaskManagerSchema]:
        query = select(cls.model).where(cls.model.id == id)
        async with db_session() as session:
            result = await session.execute(query)
            entity: Optional[TaskManager] = result.scalar_one_or_none()

            if not entity:
                return None

            return TaskManagerSchema.from_entity(entity)

    @classmethod
    async def update_task_by_id(cls, id: UUID, task: NewTaskManagerSchema) -> Optional[UUID]:
        async with db_session() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(
                    **task.model_dump()
                )
                .returning(cls.model.id)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @classmethod
    async def delete_task_from_id(cls, id: UUID) -> Optional[UUID]:
        query = delete(cls.model).where(cls.model.id == id).returning(cls.model.id)
        async with db_session() as session:
            result = await session.execute(query)
            await session.commit()
            return result.scalar()
