"""resize RAG embeddings for the local BGE model

Revision ID: c6a8f1e2d904
Revises: b7e4c9a1d203
Create Date: 2026-09-12 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
from pgvector.sqlalchemy import Vector


revision: str = "c6a8f1e2d904"
down_revision: Union[str, Sequence[str], None] = "b7e4c9a1d203"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Existing 3072-dimensional vectors cannot be cast to the new typmod.
    # RAG records are a rebuildable snapshot; business tables are untouched.
    op.execute("DELETE FROM rag_document_chunks")
    op.alter_column(
        "rag_document_chunks",
        "embedding",
        existing_type=Vector(3072),
        type_=Vector(384),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.execute("DELETE FROM rag_document_chunks")
    op.alter_column(
        "rag_document_chunks",
        "embedding",
        existing_type=Vector(384),
        type_=Vector(3072),
        existing_nullable=False,
    )