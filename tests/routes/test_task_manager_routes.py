import uuid

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from deep_medical.repos.task_manager import TaskManagerRepo
from tests.conftest import NewTaskResult


class TestCreateNewTask:

    @pytest.mark.parametrize(
        'description, completed',
        [
            (None, False),
            ("Lorep description", False),
            ("New description", True)
        ]
    )
    async def test_create_new_task(
        self,
        client: TestClient,
        get_new_task: NewTaskResult,
        description: str,
        completed: bool
    ) -> None:
        # Arrange
        payload = get_new_task(
            description=description,
            completed=completed
        ).model_dump()

        # Act
        response = client.post("/tasks/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["title"] == payload['title']
        assert response.json()["description"] == description
        assert response.json()["completed"] == completed
        assert response.json()["created_at"]
        assert response.json()["id"]

    async def test_create_new_task_failed(self, client: TestClient) -> None:
        # Arrange
        payload = {}

        # Act
        response = client.post("/tasks/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestFetchAllTasksRoute:
    async def test_fetch_all_tasks_no_data(self, client: TestClient) -> None:
        # Act
        response = client.get("/tasks/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    async def test_fetch_all_tasks_with_data(
        self,
        client: TestClient,
        get_new_task: NewTaskResult
    ) -> None:
        # Arrange
        result = await TaskManagerRepo.save(get_new_task())

        # Act
        response = client.get("/tasks/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        expected = response.json()[0]
        assert expected["title"] == result.title
        assert expected["description"] == result.description
        assert expected["completed"] == result.completed
        assert expected["id"] == str(result.id)

    @pytest.mark.parametrize(
        'completed, expected_tasks',
        [
            (False, 4),
            (True, 3),
        ]
    )
    async def test_fetch_all_tasks_based_on_completed_status(
        self,
        client: TestClient,
        get_new_task: NewTaskResult,
        completed: bool,
        expected_tasks: int
    ) -> None:
        # Arrnage
        # 3 completed: true
        for _ in range(3):
            await TaskManagerRepo.save(get_new_task(completed=True))

        # 4 completed false
        for _ in range(4):
            await TaskManagerRepo.save(get_new_task(completed=False))

        # Act
        response = client.get(f"/tasks/?completed={completed}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == expected_tasks
        for data in response.json():
            assert data["completed"] == completed

    async def test_should_raise_exception_if_completed_is_not_bool(
        self,
        client: TestClient
    ) -> None:
        # Arrange
        response = client.get("/tasks/?completed=NOT_BOOLEAN")

        # Act
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestFetchSingleTask:
    async def test_get_task_from_id_ok(
        self,
        client: TestClient,
        get_new_task: NewTaskResult
    ) -> None:
        # Arrange
        task = await TaskManagerRepo.save(get_new_task())

        # Act
        response = client.get(f"/tasks/{task.id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == str(task.id)

    async def test_should_raise_exception_if_id_not_found(
        self,
        client: TestClient
    ) -> None:
        # Act
        response = client.get(f"/tasks/{uuid.uuid4()}")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateTask:
    async def test_update_task_ok(
        self,
        client: TestClient,
        get_new_task: NewTaskResult
    ) -> None:
        # Arrange
        task = await TaskManagerRepo.save(get_new_task())
        payload = get_new_task(title="Updated title")

        # Act
        response = client.put(f"/tasks/{task.id}", json=payload.model_dump())

        # Assert
        updated_task = await TaskManagerRepo.get_task_from_id(task.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert updated_task.title == payload.title

    async def test_should_raise_exception_if_id_not_found(
        self,
        client: TestClient,
        get_new_task: NewTaskResult
    ) -> None:
        # Arrange
        payload = get_new_task(title="Updated title")

        # Act
        response = client.put(f"/tasks/{uuid.uuid4()}", json=payload.model_dump())

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_should_raise_exception_if_invalid_payload(
        self,
        client: TestClient,
        get_new_task: NewTaskResult
    ) -> None:
        # Arrange
        task = await TaskManagerRepo.save(get_new_task())
        payload = {}

        # Act
        response = client.put(f"/tasks/{task.id}", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestDeleteTask:
    async def test_delete_task(
        self,
        client: TestClient,
        get_new_task: NewTaskResult
    ) -> None:
        # Arrange
        task = await TaskManagerRepo.save(get_new_task())

        # Act
        response = client.delete(f"/tasks/{task.id}")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_should_raise_exception_if_id_not_found(self, client: TestClient) -> None:
        # Act
        response = client.delete(f"/tasks/{uuid.uuid4()}")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestPatchTask:
    async def test_patch_task_ok(
        self,
        client: TestClient,
        get_new_task: NewTaskResult
    ) -> None:
        # Arrange
        task = await TaskManagerRepo.save(get_new_task())

        # Act
        response = client.patch(f"/tasks/{task.id}", json={'completed': True})

        # Assert
        updated_task = await TaskManagerRepo.get_task_from_id(task.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert updated_task.title == task.title
        assert updated_task.completed

    async def test_should_raise_exception_if_id_not_found(
        self,
        client: TestClient,
        get_new_task: NewTaskResult
    ) -> None:
        # Arrange
        payload = get_new_task(title="Updated title")

        # Act
        response = client.patch(f"/tasks/{uuid.uuid4()}", json=payload.model_dump())

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_should_raise_exception_if_invalid_payload(
        self,
        client: TestClient,
        get_new_task: NewTaskResult
    ) -> None:
        # Arrange
        task = await TaskManagerRepo.save(get_new_task())

        # Act
        response = client.patch(f"/tasks/{task.id}", json={'title': None})

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST