"""Create Table Category

Revision ID: b112b8e3a2c8
Revises: f0d0bbf5748c
Create Date: 2023-11-24 22:45:50.551088

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b112b8e3a2c8'
down_revision: Union[str, None] = 'f0d0bbf5748c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=10), nullable=False, unique=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('user_code', sa.String(length=10), nullable=False),
        sa.Column('parent_category_code', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_code'), 'categories', ['code'], unique=True)
    op.create_index(op.f('ix_categories_user_code'), 'categories', ['user_code'])
    op.create_index(op.f('ix_categories_parent_category_code'), 'categories', ['parent_category_code'])


def downgrade():
    op.drop_table('categories')
