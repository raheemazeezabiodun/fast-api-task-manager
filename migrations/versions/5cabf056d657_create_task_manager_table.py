"""Create task_manager table

Revision ID: 5cabf056d657
Revises:
Create Date: 2025-01-30 20:23:18.825420

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '5cabf056d657'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task_manager',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=False, default=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'idx_task_manager_completed', 'task_manager', ['completed'], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_task_manager_completed', table_name='task_manager')
    op.drop_table('task_manager')
    # ### end Alembic commands ###
