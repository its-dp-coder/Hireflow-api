"""Add users table for fresh databases

Revision ID: 3b660a00074f
Revises: 9c9824b12096
Create Date: 2026-09-05
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = "3b660a00074f"
down_revision: Union[str, Sequence[str], None] = "9c9824b12096"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create users table if it does not already exist."""
    bind = op.get_bind()
    inspector = inspect(bind)

    if "users" not in inspector.get_table_names():
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("email", sa.String(), nullable=False),
            sa.Column("password_hash", sa.String(), nullable=False),
            sa.Column("full_name", sa.String(), nullable=False),
            sa.Column("role", sa.String(), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                nullable=True,
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email"),
        )

        op.create_index(
            "ix_users_id",
            "users",
            ["id"],
            unique=False,
        )

        op.create_index(
            "ix_users_email",
            "users",
            ["email"],
            unique=True,
        )


def downgrade() -> None:
    """Drop users table if it exists."""
    bind = op.get_bind()
    inspector = inspect(bind)

    if "users" in inspector.get_table_names():
        op.drop_index("ix_users_email", table_name="users")
        op.drop_index("ix_users_id", table_name="users")
        op.drop_table("users")