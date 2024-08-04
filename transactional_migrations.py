from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

def upgrade():
    conn = op.get_bind()
    with conn.begin() as transaction:
        try:
            op.create_table(
                'example_table',
                sa.Column('id', sa.Integer, primary_key=True),
                sa.Column('name', sa.String(50), nullable=False)
            )
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise

def downgrade():
    conn = op.get_bind()
    with conn.begin() as transaction:
        try:
            op.drop_table('example_table')
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise
