"""Create Table Account

Revision ID: f0d0bbf5748c
Revises: d0dbb9e15630
Create Date: 2023-11-24 20:51:56.656163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f0d0bbf5748c'
down_revision: Union[str, None] = 'd0dbb9e15630'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=10), nullable=False, unique=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=300), nullable=True),
        sa.Column('user_code', sa.String(length=10), nullable=False),
        sa.Column('balance', sa.Float(), nullable=False, default=0.0),
        sa.Column('created_at', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_code'), 'accounts', ['code'], unique=True)
    op.create_index(op.f('ix_accounts_user_code'), 'accounts', ['user_code'])


def downgrade():
    op.drop_table('users')
