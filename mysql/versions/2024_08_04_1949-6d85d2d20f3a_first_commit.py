"""First Commit

Revision ID: 6d85d2d20f3a
Revises: 
Create Date: 2024-08-04 19:49:48.925070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d85d2d20f3a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'example_table',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('example_table')