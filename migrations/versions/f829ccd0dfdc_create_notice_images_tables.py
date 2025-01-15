"""Create notice_images tables

Revision ID: f829ccd0dfdc
Revises: 36f8d00cd24b
Create Date: 2025-01-15 18:15:15.842233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision: str = 'f829ccd0dfdc'
down_revision: Union[str, None] = '36f8d00cd24b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Get the current connection
    bind = op.get_bind()
    
    # Create a reflection object
    inspector = reflection.Inspector.from_engine(bind)
    
    # Check if the 'notices' table already exists
    if 'notice_images' not in inspector.get_table_names():
        op.create_table('notice_images',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('notice_id', sa.Integer(), nullable=False),
        sa.Column('image_path', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['notice_id'], ['notices.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_notice_images_deleted_at'), 'notice_images', ['deleted_at'], unique=False)
        op.create_index(op.f('ix_notice_images_notice_id'), 'notice_images', ['notice_id'], unique=False)



def downgrade() -> None:
    op.drop_index(op.f('ix_notice_images_notice_id'), table_name='notice_images')
    op.drop_index(op.f('ix_notice_images_deleted_at'), table_name='notice_images')
    op.drop_table('notice_images')

