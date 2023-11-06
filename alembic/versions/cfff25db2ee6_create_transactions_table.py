"""create_transactions_table

Revision ID: cfff25db2ee6
Revises: ac2a188ad94d
Create Date: 2023-11-05 13:20:52.650814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'cfff25db2ee6'
down_revision: Union[str, None] = 'ac2a188ad94d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('portfolio_id', sa.Integer(), sa.ForeignKey('portfolios.id'), nullable=False),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('transaction_type', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('price_per_unit', sa.Float(), nullable=False),
        sa.Column('fees', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('transactions')
