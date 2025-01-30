from sqlmodel import Field
from sqlalchemy import Index, PrimaryKeyConstraint

from deep_medical.models import mixins


class TaskManager(mixins.IdMixin, mixins.TimestampsMixin, table=True):
    __tablename__ = 'task_manager'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        Index('idx_task_manager_completed', 'completed')
    )

    title: str = Field(nullable=False)
    description: str = Field(nullable=True)
    completed: bool = False
