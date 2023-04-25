"""create_companies_table

Revision ID: 019cd333c5e6
Revises: 
Create Date: 2023-04-25 18:08:19.213294

"""
from alembic import op
from uuid import uuid4
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '019cd333c5e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    table = op.create_table(
        'companies',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('mode', sa.Enum('active', 'inactive', name='company_mode'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('companies')
    pass
