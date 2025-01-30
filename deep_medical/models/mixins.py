from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlmodel import Field, SQLModel


class IdMixin(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)


class TimestampsMixin(SQLModel):
    created_at: datetime = Field(
        nullable=False,
        default_factory=datetime.utcnow,
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=sa.Column(
            sa.DateTime(timezone=False),
            onupdate=datetime.utcnow,
            nullable=False,
        ),
    )