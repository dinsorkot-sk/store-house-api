"""create contacts table

Revision ID: 85aa01b905dd
Revises: 5daaf8724616
Create Date: 2025-01-22 15:24:16.571188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision: str = '85aa01b905dd'
down_revision: Union[str, None] = '5daaf8724616'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     # Get the current connection
    bind = op.get_bind()

    # Create a reflection object
    inspector = reflection.Inspector.from_engine(bind)

    # Check if the 'notices' table already exists
    if "contacts" not in inspector.get_table_names():
        op.create_table(
            'contacts',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('order_number', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=255), nullable=False),
            sa.Column('url', sa.Text(), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
            sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

        op.create_index('contacts_deleted_at', 'contacts', ['deleted_at'])


def downgrade() -> None:
    op.drop_index('contacts_deleted_at', table_name='contacts')
    op.drop_table('contacts')
