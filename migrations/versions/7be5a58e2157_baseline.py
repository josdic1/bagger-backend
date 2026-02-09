"""baseline

Revision ID: 7be5a58e2157
Revises: 1f0bf593a424
Create Date: 2026-02-09 18:56:08.407964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7be5a58e2157'
down_revision: Union[str, Sequence[str], None] = '1f0bf593a424'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
