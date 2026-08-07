"""create catalog tables

Revision ID: 202608060001
Revises:
Create Date: 2026-08-06 00:00:00
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "202608060001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "partners",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("slug", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("ix_partners_slug", "partners", ["slug"])
    op.create_table(
        "titles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("partner_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("partner_title_id", sa.String(length=128), nullable=False),
        sa.Column("display_title", sa.String(length=512), nullable=False),
        sa.Column("source_language", sa.String(length=3), nullable=False),
        sa.Column("maturity_rating", sa.String(length=16), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["partner_id"], ["partners.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("partner_id", "partner_title_id"),
    )
    op.create_index("ix_titles_partner_id", "titles", ["partner_id"])
    op.create_table(
        "rights_grants",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("territory", sa.String(length=16), nullable=False),
        sa.Column("surface", sa.String(length=32), nullable=False),
        sa.Column("valid_from", sa.Date(), nullable=False),
        sa.Column("valid_until", sa.Date(), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["title_id"], ["titles.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title_id", "territory", "surface", "valid_from"),
    )
    op.create_index("ix_rights_grants_surface", "rights_grants", ["surface"])
    op.create_index("ix_rights_grants_territory", "rights_grants", ["territory"])
    op.create_index("ix_rights_grants_title_id", "rights_grants", ["title_id"])


def downgrade() -> None:
    op.drop_table("rights_grants")
    op.drop_table("titles")
    op.drop_table("partners")
