"""create_users_table

Revision ID: 1116dcc4acd7
Revises: 019cd333c5e6
Create Date: 2023-04-26 00:24:59.826398

"""
from alembic import op
from uuid import uuid4
import sqlalchemy as sa
from schemas.user import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD


# revision identifiers, used by Alembic.
revision = '1116dcc4acd7'
down_revision = '019cd333c5e6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    table = op.create_table(
        'users',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(128), nullable=False),
        sa.Column('email', sa.String(128), nullable=False, unique=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('company_id', sa.UUID, sa.ForeignKey('companies.id'), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('is_admiln', sa.Boolean, nullable=False, default=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('last_name'), 'users', ['last_name'], unique=False)
    
    # Create 1 record in companies table
    company = op.bulk_insert(
        'companies',
        [
            {
                'id': uuid4(),
                'name': 'Nashtech Global',
                'description': 'Nashtech Global is a global software outsourcing company with more than 20 years of experience in the IT industry. We provide full lifecycle services from consulting, solution designing, development, testing and maintenance & support for applications across various business areas.',
                'mode': 'active',
            }
        ]
    )

    user = op.bulk_insert(
        'users',
        [
            {
                'id': uuid4(),
                'username': 'admin',
                'email': 'ngtrdai@hotmail.com',
                'first_name': 'Dai',
                'last_name': 'Nguyen',
                'company_id': company.inserted_primary_key[0]['id'],
                'is_active': True,
                'is_admin': True,
                'hashed_password': 'aaa'
            }
        ]
    )

def downgrade() -> None:
    op.drop_table('users')
