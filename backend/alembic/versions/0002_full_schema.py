"""full schema

Revision ID: 0002
Revises: 0001
Create Date: 2026-03-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import uuid

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('languages',
        sa.Column('id', sa.Uuid(), nullable=False, default=uuid.uuid4),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('emoji', sa.String(10), nullable=False, server_default='🌐'),
        sa.Column('direction_mode', sa.Enum('front_to_back', 'back_to_front', 'random', name='directionmode'), nullable=False, server_default='front_to_back'),
        sa.Column('target_lang', sa.String(10), nullable=False, server_default='cs'),
        sa.Column('order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('lessons',
        sa.Column('id', sa.Uuid(), nullable=False, default=uuid.uuid4),
        sa.Column('language_id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('direction_mode', sa.Enum('front_to_back', 'back_to_front', 'random', 'inherit', name='lessondirectionmode'), nullable=False, server_default='inherit'),
        sa.Column('order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['language_id'], ['languages.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('cards',
        sa.Column('id', sa.Uuid(), nullable=False, default=uuid.uuid4),
        sa.Column('lesson_id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('card_fields',
        sa.Column('id', sa.Uuid(), nullable=False, default=uuid.uuid4),
        sa.Column('card_id', sa.Uuid(), nullable=False),
        sa.Column('label', sa.String(50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False, server_default=''),
        sa.Column('order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_tested', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('image_path', sa.String(500), nullable=True),
        sa.Column('audio_path', sa.String(500), nullable=True),
        sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('card_progress',
        sa.Column('id', sa.Uuid(), nullable=False, default=uuid.uuid4),
        sa.Column('card_id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('direction', sa.Enum('front_to_back', 'back_to_front', name='progressdirection'), nullable=False),
        sa.Column('interval', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('ease_factor', sa.Float(), nullable=False, server_default='2.5'),
        sa.Column('repetitions', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('last_reviewed', sa.DateTime(), nullable=True),
        sa.Column('is_learned', sa.Boolean(), nullable=False, server_default='false'),
        sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('card_progress')
    op.drop_table('card_fields')
    op.drop_table('cards')
    op.drop_table('lessons')
    op.drop_table('languages')
    op.execute('DROP TYPE IF EXISTS progressdirection')
    op.execute('DROP TYPE IF EXISTS lessondirectionmode')
    op.execute('DROP TYPE IF EXISTS directionmode')
