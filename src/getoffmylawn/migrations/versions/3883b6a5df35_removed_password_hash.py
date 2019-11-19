"""Removed password hash.

Revision ID: 3883b6a5df35
Revises: 6781acfc7c14
Create Date: 2019-11-12 22:49:40.682544

"""
from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "3883b6a5df35"
down_revision = "6781acfc7c14"
branch_labels = None
depends_on = None


def upgrade():  # noqa: D103
    op.drop_column("users", "password_hash")


def downgrade():  # noqa: D103
    op.add_column(
        "users",
        sa.Column("password_hash", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
