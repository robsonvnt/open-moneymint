"""Add unique constraint to portfolio_code and date

Revision ID: c58b546b240b
Revises: f608c441eac3
Create Date: 2023-11-09 11:41:15.124637

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c58b546b240b'
down_revision: Union[str, None] = 'f608c441eac3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_unique_constraint(
        'unique_portfolio_code_date', 'consolidated_balance_portfolios', ['portfolio_code', 'date']
    )


def downgrade():
    op.drop_constraint(
        'unique_portfolio_code_date', 'consolidated_balance_portfolios', type_='unique'
    )
