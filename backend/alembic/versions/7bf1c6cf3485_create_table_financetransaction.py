"""Create Table FinanceTransaction

Revision ID: 7bf1c6cf3485
Revises: b112b8e3a2c8
Create Date: 2023-11-25 14:43:28.604186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bf1c6cf3485'
down_revision: Union[str, None] = 'b112b8e3a2c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'finances_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=10), nullable=False, unique=True),
        sa.Column('account_code', sa.String(length=10), nullable=False),
        sa.Column('description', sa.String(length=300), nullable=False),
        sa.Column('category_code', sa.String(length=10), nullable=False),
        sa.Column('type', sa.String(length=100), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_finances_transactions_code'), 'finances_transactions', ['code'], unique=True)
    op.create_index(op.f('ix_finances_transactions_account_code'), 'finances_transactions', ['account_code'])
    op.create_index(op.f('ix_finances_transactions_category_code'), 'finances_transactions', ['category_code'])
    op.create_index(op.f('ix_finances_transactions_type'), 'finances_transactions', ['type'])
    op.create_index(op.f('ix_finances_transactions_date'), 'finances_transactions', ['date'])


def downgrade():
    op.drop_table('finances_transactions')
