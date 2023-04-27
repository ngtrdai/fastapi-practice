"""migration_v1

Revision ID: 8606974d2aa7
Revises: 
Create Date: 2023-04-27 22:33:34.200717

"""
from alembic import op
from uuid import uuid4
import sqlalchemy as sa
from schemas.user import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD


# revision identifiers, used by Alembic.
revision = '8606974d2aa7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Companies table
    companies_table = op.create_table(
        'companies',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('mode', sa.Enum('active', 'inactive', name='company_mode'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_index(op.f('ix_companies_name'), 'companies', ['name'], unique=True)

    # Users table
    users_table = op.create_table(
        'users',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(128), nullable=False),
        sa.Column('email', sa.String(128), nullable=False, unique=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('company_id', sa.UUID, sa.ForeignKey('companies.id'), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('is_admin', sa.Boolean, nullable=False, default=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('last_name'), 'users', ['last_name'], unique=False)

    # Tasks table
    tasks_table = op.create_table(
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

    # Seed data
    company_id = str(uuid4())
    op.bulk_insert(
        companies_table,
        [
            {
                'id': company_id,
                'name': 'NashTech Vietnam',
                'description': 'NashTech Vietnam description',
                'mode': 'active',
            }
        ]
    )

    op.bulk_insert(
        users_table,
        [
            {
                'id': str(uuid4()),
                'username': 'admin',
                'hashed_password': get_password_hash(ADMIN_DEFAULT_PASSWORD),
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'Demo',
                'company_id': company_id,
                'is_active': True,
                'is_admin': True,
            }
        ]
    )

def downgrade() -> None:
    op.drop_index(op.f('ix_companies_name'), table_name='companies')
    op.drop_table('companies')

    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('first_name'), table_name='users')
    op.drop_index(op.f('last_name'), table_name='users')
    op.drop_table('users')

    op.drop_index(op.f('ix_tasks_summary'), table_name='tasks')
    op.drop_table('tasks')
