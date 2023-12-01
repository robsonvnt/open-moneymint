"""create_investments_table

Revision ID: ac2a188ad94d
Revises: 9268a3ce93b3
Create Date: 2023-11-05 13:20:02.169088

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ac2a188ad94d'
down_revision: Union[str, None] = '9268a3ce93b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'investments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=10), nullable=False, unique=True),
        sa.Column('portfolio_code', sa.String(length=10), nullable=False),
        sa.Column('asset_type', sa.String(), nullable=False),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('purchase_price', sa.Float(), nullable=False),
        sa.Column('current_average_price', sa.Float(), nullable=True),
        sa.Column('purchase_date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('investments')
