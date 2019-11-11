"""users.

Revision ID: 17de12da1127
Revises:
Create Date: 2019-04-26 19:03:11.540559

"""
from alembic import op
from sqlalchemy.dialects import postgresql

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "17de12da1127"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():  # noqa: D103
    op.execute('CREATE EXTENSION "pgcrypto"')
    op.create_table(
        "users",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("username", sa.String, nullable=False),
        sa.Column("password_hash", sa.String, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )


def downgrade():  # noqa: D103
    op.drop_table("users")
