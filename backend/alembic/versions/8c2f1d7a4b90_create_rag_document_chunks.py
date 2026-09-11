"""create RAG document chunks table

Revision ID: 8c2f1d7a4b90
Revises: 4b9d8922b156
Create Date: 2026-09-12 02:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


revision: str = "8c2f1d7a4b90"
down_revision: Union[str, Sequence[str], None] = "4b9d8922b156"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "rag_document_chunks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("embedding", Vector(3072), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_rag_document_chunks_source",
        "rag_document_chunks",
        ["source"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_rag_document_chunks_source", table_name="rag_document_chunks")
    op.drop_table("rag_document_chunks")