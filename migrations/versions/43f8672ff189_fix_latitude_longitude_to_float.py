"""fix latitude longitude to float

Revision ID: 43f8672ff189
Revises: ffeb8db1d177
Create Date: 2026-04-09 16:27:14.707129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43f8672ff189'
down_revision: Union[str, Sequence[str], None] = 'ffeb8db1d177'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 🔴 Remover FK antes de dropar tabelas
    op.drop_constraint(
        'empresa_tipo_servico_tipo_servico_id_fkey',
        'empresa_tipo_servico',
        type_='foreignkey'
    )

    op.drop_constraint(
        'empresa_tipo_servico_empresa_id_fkey',
        'empresa_tipo_servico',
        type_='foreignkey'
    )

    # Agora pode dropar as tabelas com segurança
    op.drop_index(op.f('ix_tipos_servico_id'), table_name='tipos_servico')
    op.drop_table('tipos_servico')
    op.drop_table('empresa_tipo_servico')

    op.alter_column(
        'empresas',
        'telefone',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    op.drop_constraint(
        op.f('servicos_empresa_id_fkey'),
        'servicos',
        type_='foreignkey'
    )

    op.drop_column('servicos', 'empresa_id')


def downgrade() -> None:
    """Downgrade schema."""

    op.add_column(
        'servicos',
        sa.Column('empresa_id', sa.INTEGER(), autoincrement=False, nullable=True)
    )

    op.create_foreign_key(
        op.f('servicos_empresa_id_fkey'),
        'servicos',
        'empresas',
        ['empresa_id'],
        ['id']
    )

    op.alter_column(
        'empresas',
        'telefone',
        existing_type=sa.VARCHAR(),
        nullable=False
    )

    # Recria tabelas na ordem correta
    op.create_table(
        'tipos_servico',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('tipos_servico_pkey'))
    )

    op.create_index(
        op.f('ix_tipos_servico_id'),
        'tipos_servico',
        ['id'],
        unique=False
    )

    op.create_table(
        'empresa_tipo_servico',
        sa.Column('empresa_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('tipo_servico_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ['empresa_id'],
            ['empresas.id'],
            name=op.f('empresa_tipo_servico_empresa_id_fkey')
        ),
        sa.ForeignKeyConstraint(
            ['tipo_servico_id'],
            ['tipos_servico.id'],
            name=op.f('empresa_tipo_servico_tipo_servico_id_fkey')
        ),
        sa.PrimaryKeyConstraint(
            'empresa_id',
            'tipo_servico_id',
            name=op.f('empresa_tipo_servico_pkey')
        )
    )