from __future__ import annotations
import os
from dataclasses import asdict
from sqlalchemy import func
from pgvector.sqlalchemy import Vector

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, sessionmaker, Session

from dotenv import load_dotenv

from src.db import schemas
from src.db.vectorized_postgres_engine import get_vectorized_postgres_engine, EngineParams
from src.utils.tokenizer import broadcast, EMBEDDING_SHAPE

load_dotenv('src/db/.env')

HOST = os.environ.get("DB_HOST")
PORT = os.environ.get("DB_PORT")
USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

engine_params = EngineParams(host=HOST, port=PORT, user=USER, password=PASSWORD, db_name=DB_NAME)
engine = get_vectorized_postgres_engine(engine_params)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=AsyncSession)

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class Base(DeclarativeBase, MappedAsDataclass):
    pass

class DBEmbedding(Base):
    __tablename__ = "db_embeddings"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    embeddings: Mapped[Vector] = mapped_column(Vector(EMBEDDING_SHAPE))

    def to_dict(self):
        return asdict(self)
    
async def create_embedding(db: AsyncSession, embedding: schemas.EmbeddingSchema):
    db_embedding = DBEmbedding(**embedding.dict())
    db.add(db_embedding)
    await db.commit()
    # db.refresh()
    return db_embedding

