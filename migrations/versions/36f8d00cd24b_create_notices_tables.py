"""Create notices tables

Revision ID: 36f8d00cd24b
Revises: 
Create Date: 2025-01-15 18:14:14.284450

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision: str = "36f8d00cd24b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Get the current connection
    bind = op.get_bind()

    # Create a reflection object
    inspector = reflection.Inspector.from_engine(bind)

    # Check if the 'notices' table already exists
    if "notices" not in inspector.get_table_names():
        op.create_table(
            "notices",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("title", sa.String(length=255), nullable=False),
            sa.Column("first_name", sa.String(length=100), nullable=False),
            sa.Column("last_name", sa.String(length=100), nullable=False),
            sa.Column("phone", sa.String(length=20), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=True),
            sa.Column("location", sa.Text(), nullable=False),
            sa.Column("size", sa.String(length=50), nullable=True),
            sa.Column("office_size", sa.String(length=50), nullable=True),
            sa.Column("details", sa.Text(), nullable=True),
            sa.Column("preferred_contact_phone", sa.Boolean(), nullable=True),
            sa.Column("preferred_contact_email", sa.Boolean(), nullable=True),
            sa.Column("poster_type", sa.String(length=50), nullable=True),
            sa.Column("price", sa.DECIMAL(), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=True,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=True,
            ),
            sa.Column("deleted_at", sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_notices_deleted_at"), "notices", ["deleted_at"], unique=False
        )
        op.create_index(op.f("ix_notices_email"), "notices", ["email"], unique=False)
        op.create_index(
            op.f("ix_notices_location"), "notices", ["location"], unique=False
        )
        op.create_index(op.f("ix_notices_phone"), "notices", ["phone"], unique=False)
        op.create_index(op.f("ix_notices_title"), "notices", ["title"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_notices_title"), table_name="notices")
    op.drop_index(op.f("ix_notices_phone"), table_name="notices")
    op.drop_index(op.f("ix_notices_location"), table_name="notices")
    op.drop_index(op.f("ix_notices_email"), table_name="notices")
    op.drop_index(op.f("ix_notices_deleted_at"), table_name="notices")
    op.drop_table("notices")
