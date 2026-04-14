"""file-visibility

Revision ID: 9ff088e197e4
Revises: 7aa7418c1dea
Create Date: 2026-04-14 07:14:04.424025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ff088e197e4'
down_revision: Union[str, None] = '7aa7418c1dea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Define enum once so it's reusable
file_visibility_enum = sa.Enum('private', 'public', name='filevisibility')


def upgrade() -> None:
    """Upgrade schema."""

    # 1. Create enum type (Postgres-specific)
    bind = op.get_bind()
    file_visibility_enum.create(bind, checkfirst=True)

    # 2. Add column as nullable first
    op.add_column(
        'storage_objects',
        sa.Column('visibility', file_visibility_enum, nullable=True)
    )

    # 3. Backfill existing rows
    op.execute(
        "UPDATE storage_objects SET visibility = 'private'"
    )

    # 4. Enforce NOT NULL constraint
    op.alter_column(
        'storage_objects',
        'visibility',
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""

    # 1. Drop column
    op.drop_column('storage_objects', 'visibility')

    # 2. Drop enum type
    bind = op.get_bind()
    file_visibility_enum.drop(bind, checkfirst=True)