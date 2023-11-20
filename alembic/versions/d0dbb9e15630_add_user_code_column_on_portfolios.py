"""Add user code column on portfolios

Revision ID: d0dbb9e15630
Revises: f58bdd078dfd
Create Date: 2023-11-18 12:24:34.866407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd0dbb9e15630'
down_revision: Union[str, None] = 'f58bdd078dfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Comando para adicionar a coluna 'user_code' à tabela 'portfolios'
    op.add_column('portfolios', sa.Column('user_code', sa.String(length=10), nullable=True))


def downgrade() -> None:
    # Comando para remover a coluna 'user_code' da tabela 'portfolios'
    op.drop_column('portfolios', 'user_code')
