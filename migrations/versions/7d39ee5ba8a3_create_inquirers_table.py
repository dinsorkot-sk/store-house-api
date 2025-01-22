"""create inquirers table

Revision ID: 7d39ee5ba8a3
Revises: f829ccd0dfdc
Create Date: 2025-01-19 18:42:52.659979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision: str = '7d39ee5ba8a3'
down_revision: Union[str, None] = 'f829ccd0dfdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Get the current connection
    bind = op.get_bind()

    # Create a reflection object
    inspector = reflection.Inspector.from_engine(bind)

    # Check if the 'notices' table already exists
    if "inquirers" not in inspector.get_table_names():
        op.create_table(
            'inquirers',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('notice_id', sa.Integer(), nullable=False),
            sa.Column('full_name', sa.String(length=255), nullable=False),
            sa.Column('phone_number', sa.String(length=10), nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('detail', sa.Text(), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
            sa.Column('uploaded_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['notice_id'], ['notices.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

        op.create_index('inquirers_index_8', 'inquirers', ['notice_id'])
        op.create_index('inquirers_index_9', 'inquirers', ['deleted_at'])


def downgrade() -> None:
    op.drop_index('inquirers_index_9', table_name='inquirers')
    op.drop_index('inquirers_index_8', table_name='inquirers')
    op.drop_table('inquirers')
