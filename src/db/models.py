from __future__ import annotations

from dataclasses import asdict

from pgvector.sqlalchemy import Vector

from sqlalchemy import Index
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

from vectorized_postgres_engine import get_vectorized_postgres_engine

EMBEDDING_SHAPE = 8192

class Base(DeclarativeBase, MappedAsDataclass):
    pass

class DBEmbedding(Base):
    __tablename__ = "db_embeddings"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    embeddings: Mapped[Vector] = mapped_column(Vector(EMBEDDING_SHAPE))

    def to_dict(self):
        return asdict(self)
