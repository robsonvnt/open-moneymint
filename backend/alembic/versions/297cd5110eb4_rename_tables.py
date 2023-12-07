"""Rename tables

Revision ID: 297cd5110eb4
Revises: 7bf1c6cf3485
Create Date: 2023-11-28 11:47:57.791762

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '297cd5110eb4'
down_revision: Union[str, None] = '7bf1c6cf3485'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Comando para renomear a tabela
    op.rename_table('consolidated_balance_portfolios', 'investments_consolidated_balance_portfolios')
    op.rename_table('portfolios', 'investments_portfolios')
    op.rename_table('transactions', 'investments_transactions')

    # Domain finances
    op.rename_table('categories', 'finances_categories')
    op.rename_table('accounts', 'finances_accounts')

    # Auth
    op.rename_table('users', 'auth_users')

def downgrade():
    # Comando reverso para renomear a tabela de volta ao nome original
    op.rename_table('investments_consolidated_balance_portfolios', 'consolidated_balance_portfolios')
    op.rename_table('investments_portfolios', 'portfolios')
    op.rename_table('investments_transactions', 'transactions')

    # Domain finances
    op.rename_table('finances_categories', 'categories')
    op.rename_table('finances_accounts', 'accounts')

    # Auth
    op.rename_table('auth_users', 'users')
