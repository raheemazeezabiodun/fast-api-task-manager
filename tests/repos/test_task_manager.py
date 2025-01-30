import uuid

import pytest

from deep_medical.repos.task_manager import TaskManagerRepo
from tests.conftest import NewTaskResult


class TestTaskManagerRepo:

    @pytest.mark.parametrize(
        'description, completed',
        [
            (None, False),
            ("Lorep description", False),
            ("New description", True)
        ]
    )
    async def test_save(
            self,
            get_new_task: NewTaskResult,
            description: str,
            completed: bool
    ) -> None:
        # Arrange
        payload = get_new_task(description=description, completed=completed)

        # Act
        task = await TaskManagerRepo.save(payload)

        # Assert
        assert task
        assert task.id
        assert task.description == description
        assert task.completed == completed
        assert task.title == payload.title

    async def test_get_tasks(self, get_new_task: NewTaskResult) -> None:
        # Arrange
        await TaskManagerRepo.save(get_new_task())
        await TaskManagerRepo.save(get_new_task())

        # Act
        tasks = await TaskManagerRepo.get_tasks()

        # Assert
        assert len(tasks) == 2

    async def test_get_tasks_from_id(self, get_new_task: NewTaskResult) -> None:
        # Arrange
        task = await TaskManagerRepo.save(get_new_task())

        # Act
        result = await TaskManagerRepo.get_task_from_id(task.id)

        # Assert
        assert result.id == task.id
        assert result.title == task.title

    async def test_get_tasks_from_id_not_exists(self) -> None:
        # Act
        result = await TaskManagerRepo.get_task_from_id(uuid.uuid4())

        # Assert
        assert not result

    async def test_delete_task_from_id(self, get_new_task: NewTaskResult) -> None:
        # Arrange
        task = await TaskManagerRepo.save(get_new_task())

        # Act
        deleted_id = await TaskManagerRepo.delete_task_from_id(task.id)

        # Assert
        assert deleted_id == task.id

    async def test_delete_task_from_id_not_exists(self) -> None:
        # Act
        result = await TaskManagerRepo.delete_task_from_id(uuid.uuid4())

        # Assert
        assert not result

    async def test_update_task_by_id(self, get_new_task: NewTaskResult) -> None:
        # Arrange
        task = await TaskManagerRepo.save(get_new_task())
        payload = get_new_task(title="Updated Title")

        # Act
        updated_task_id = await TaskManagerRepo.update_task_by_id(task.id, payload)

        # Assert
        updated_task = await TaskManagerRepo.get_task_from_id(task.id)
        assert updated_task_id == task.id
        assert updated_task.title == payload.title

    async def test_update_task_by_id_not_exists(self, get_new_task: NewTaskResult) -> None:
        # Act
        result = await TaskManagerRepo.update_task_by_id(uuid.uuid4(), get_new_task())

        # Assert
        assert not result
