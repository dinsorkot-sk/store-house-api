"""create working_images table

Revision ID: 6cdde3621fce
Revises: 4314b87e3ada
Create Date: 2025-01-24 12:53:27.967410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision: str = '6cdde3621fce'
down_revision: Union[str, None] = '4314b87e3ada'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create working_images table
    # Get the current connection
    bind = op.get_bind()

    # Create a reflection object
    inspector = reflection.Inspector.from_engine(bind)

    # Check if the 'working_images' table already exists
    if "working_images" not in inspector.get_table_names():
        op.create_table(
            'working_images',
            sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('working_id', sa.Integer, sa.ForeignKey('working.id'), nullable=False),
            sa.Column('working_image_data', sa.Text, nullable=False),
            sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
            sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
            sa.Column('deleted_at', sa.TIMESTAMP, nullable=True),
        )
        # Create indexes
        op.create_index('images_working_index', 'working_images', ['working_id'])
        op.create_index('working_index', 'working_images', ['deleted_at'])

def downgrade() -> None:
    # Drop indexes and table
    op.drop_index('working_index', table_name='working_images')
    op.drop_index('images_working_index', table_name='working_images')
    op.drop_table('working_images')
