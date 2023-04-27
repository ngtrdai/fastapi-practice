"""create_tasks_table

Revision ID: 9a27ff3566f6
Revises: 1116dcc4acd7
Create Date: 2023-04-26 14:24:31.386879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a27ff3566f6'
down_revision = '1116dcc4acd7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    table = op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('summary', sa.String(50), nullable=False),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('status', sa.Enum('new', 'in progress', 'completed', 'archived', name='task_status'), nullable=False),
        sa.Column('priority', sa.Enum('low', 'medium', 'high', name='task_priority'), nullable=False),
        sa.Column('owner_id', sa.UUID, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_index(op.f('ix_tasks_summary'), 'tasks', ['summary'], unique=False)

def downgrade() -> None:
    op.drop_table('tasks')

