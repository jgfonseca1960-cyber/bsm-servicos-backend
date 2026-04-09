"""add servico_id

Revision ID: ffeb8db1d177
Revises: 
Create Date: 2026-04-09 16:13:03.083989
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffeb8db1d177'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ✅ Adiciona a coluna servico_id
    op.add_column(
        'empresas',
        sa.Column('servico_id', sa.Integer(), nullable=True)
    )

    # ✅ Cria a chave estrangeira
    op.create_foreign_key(
        'fk_empresas_servico',
        'empresas',
        'servicos',
        ['servico_id'],
        ['id']
    )


def downgrade() -> None:
    """Downgrade schema."""

    # 🔄 Remove a FK
    op.drop_constraint(
        'fk_empresas_servico',
        'empresas',
        type_='foreignkey'
    )

    # 🔄 Remove a coluna
    op.drop_column('empresas', 'servico_id')