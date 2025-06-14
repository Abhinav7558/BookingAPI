"""Renamed datetime field to scheduled_at

Revision ID: 7f0fd7e50b9f
Revises: 508e55f11909
Create Date: 2025-06-08 18:15:32.289980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f0fd7e50b9f'
down_revision: Union[str, None] = '508e55f11909'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('classes', sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=False))
    op.drop_index(op.f('ix_classes_datetime'), table_name='classes')
    op.create_index(op.f('ix_classes_scheduled_at'), 'classes', ['scheduled_at'], unique=False)
    op.drop_column('classes', 'datetime')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('classes', sa.Column('datetime', sa.DATETIME(), nullable=False))
    op.drop_index(op.f('ix_classes_scheduled_at'), table_name='classes')
    op.create_index(op.f('ix_classes_datetime'), 'classes', ['datetime'], unique=False)
    op.drop_column('classes', 'scheduled_at')
    # ### end Alembic commands ###
