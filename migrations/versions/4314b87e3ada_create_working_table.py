"""create working table

Revision ID: 4314b87e3ada
Revises: b8b3849aab4c
Create Date: 2025-01-24 12:42:56.450287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision: str = '4314b87e3ada'
down_revision: Union[str, None] = 'b8b3849aab4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Create working table
    # Get the current connection
    bind = op.get_bind()

    # Create a reflection object
    inspector = reflection.Inspector.from_engine(bind)

    # Check if the 'working' table already exists
    if "working" not in inspector.get_table_names():
        op.create_table(
            'working',
            sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('working_name', sa.Text, nullable=False),
            sa.Column('detail', sa.Text, nullable=True),
            sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
            sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
            sa.Column('deleted_at', sa.TIMESTAMP, nullable=True),
        )
        # Create index on deleted_at column
        op.create_index('messages_index', 'working', ['deleted_at'])

def downgrade():
    # Drop the index
    op.drop_index('messages_index', table_name='working')
    # Drop the table
    op.drop_table('working')
