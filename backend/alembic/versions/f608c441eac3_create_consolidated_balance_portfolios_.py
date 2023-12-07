"""create_consolidated_balance_portfolios_table

Revision ID: f608c441eac3
Revises: cfff25db2ee6
Create Date: 2023-11-05 13:21:46.183852

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f608c441eac3'
down_revision: Union[str, None] = 'cfff25db2ee6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'consolidated_balance_portfolios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('portfolio_code', sa.String(length=10), sa.ForeignKey('portfolios.code'), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('balance', sa.Float(), nullable=False),
        sa.Column('amount_invested', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('consolidated_balance_portfolios')
