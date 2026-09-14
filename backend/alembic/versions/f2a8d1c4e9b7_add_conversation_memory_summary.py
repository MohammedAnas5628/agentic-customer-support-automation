"""add rolling conversation memory summary

Revision ID: f2a8d1c4e9b7
Revises: c6a8f1e2d904
Create Date: 2026-09-14 00:00:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "f2a8d1c4e9b7"
down_revision: Union[str, Sequence[str], None] = "c6a8f1e2d904"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("conversations", sa.Column("memory_summary", sa.Text(), nullable=True))
    op.add_column("conversations", sa.Column("summary_through_message_id", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("conversations", "summary_through_message_id")
    op.drop_column("conversations", "memory_summary")