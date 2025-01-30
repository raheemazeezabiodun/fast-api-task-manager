from typing import Callable
from typing import Optional

import pytest

from deep_medical.schemas.task_manager import NewTaskManagerSchema


NewTaskResult = Callable[..., NewTaskManagerSchema]


@pytest.fixture(scope="function")
def get_new_task() -> NewTaskResult:
    def func(
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: bool = False
    ) -> NewTaskManagerSchema:
        return NewTaskManagerSchema(
            title=title or "Random Title",
            description=description,
            completed=completed
        )

    return func
