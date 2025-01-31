"""create contact_images table

Revision ID: b8b3849aab4c
Revises: 85aa01b905dd
Create Date: 2025-01-22 15:37:54.664186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision: str = 'b8b3849aab4c'
down_revision: Union[str, None] = '85aa01b905dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     # Get the current connection
    bind = op.get_bind()

    # Create a reflection object
    inspector = reflection.Inspector.from_engine(bind)

    # Check if the 'notices' table already exists
    if "contact_images" not in inspector.get_table_names():
        op.create_table(
            'contact_images',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('contact_id', sa.Integer(), nullable=False),
            sa.Column('image_path', sa.String(length=255), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
            sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

        op.create_index('contact_images_contact_id', 'contact_images', ['contact_id'])
        op.create_index('contact_images_deleted_at', 'contact_images', ['deleted_at'])

def downgrade() -> None:
    op.drop_index('contact_images_contact_id', table_name='contact_images')
    op.drop_index('contact_images_deleted_at', table_name='contact_images')
    op.drop_table('contact_images')
