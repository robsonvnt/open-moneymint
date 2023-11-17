"""Create User Table

Revision ID: f58bdd078dfd
Revises: c58b546b240b
Create Date: 2023-11-17 09:07:47.078192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f58bdd078dfd'
down_revision: Union[str, None] = 'c58b546b240b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=10), nullable=False, unique=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('login', sa.String(length=30), nullable=False, unique=True),
        sa.Column('password', sa.String(length=60), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_code'), 'users', ['code'], unique=True)
    op.create_index(op.f('ix_users_login'), 'users', ['login'], unique=True)


def downgrade():
    op.drop_table('users')
