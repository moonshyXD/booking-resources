"""Initial

Revision ID: e8f4a7a6a3e3
Revises: 
Create Date: 2024-05-21 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'e8f4a7a6a3e3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    resource_status_enum = postgresql.ENUM(
        "FREE",
        "FULL",
        "MAINTENANCE",
        "DELETED",
        name="resourcestatus",
        create_type=False,
    )
    resource_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "resource_categories",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "resources",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("company_id", sa.UUID(), nullable=False),
        sa.Column("category_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("info", sa.Text(), nullable=True),
        sa.Column("photo_url", sa.String(length=255), nullable=True),
        sa.Column("status", resource_status_enum, server_default=sa.text("'FREE'"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["resource_categories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("resources")
    op.drop_table("resource_categories")
    postgresql.ENUM(name="resourcestatus").drop(op.get_bind(), checkfirst=True)
