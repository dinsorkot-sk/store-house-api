"""create admin_users table

Revision ID: 5daaf8724616
Revises: 7d39ee5ba8a3
Create Date: 2025-01-20 13:33:29.612240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision: str = '5daaf8724616'
down_revision: Union[str, None] = '7d39ee5ba8a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = '5daaf8724616'
down_revision: Union[str, None] = '7d39ee5ba8a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create admin_users table
     # Get the current connection
    bind = op.get_bind()

    # Create a reflection object
    inspector = reflection.Inspector.from_engine(bind)

    # Check if the 'notices' table already exists
    if "admin_users" not in inspector.get_table_names():
        op.create_table(
            'admin_users',
            sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('username', sa.String(50), nullable=False, unique=True),
            sa.Column('password', sa.String(255), nullable=False),
            sa.Column(
                'created_at',
                sa.TIMESTAMP,
                server_default=sa.text('CURRENT_TIMESTAMP')
            ),
            sa.Column(
                'updated_at',
                sa.TIMESTAMP,
                server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
            ),
            sa.Column('deleted_at', sa.TIMESTAMP, nullable=True),
        )
        # Create index on deleted_at column
        op.create_index('admin_index', 'admin_users', ['deleted_at'])


def downgrade():
    # Drop the index
    op.drop_index('admin_index', table_name='admin_users')
    # Drop the table
    op.drop_table('admin_users')
