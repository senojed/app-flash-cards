"""initial

Revision ID: 0001
Revises:
Create Date: 2026-03-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import uuid

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Uuid(), nullable=False, default=uuid.uuid4),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )


def downgrade() -> None:
    op.drop_table('users')
