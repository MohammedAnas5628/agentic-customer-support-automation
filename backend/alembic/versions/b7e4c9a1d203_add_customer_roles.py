"""add customer roles

Revision ID: b7e4c9a1d203
Revises: 8c2f1d7a4b90
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7e4c9a1d203"
down_revision: Union[str, Sequence[str], None] = "8c2f1d7a4b90"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "customers",
        sa.Column("role", sa.String(length=20), server_default="customer", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("customers", "role")