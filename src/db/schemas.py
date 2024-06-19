from pydantic import BaseModel
from pgvector.sqlalchemy import Vector

class EmbeddingSchema(BaseModel):
    name: str
    embeddings: list[float]

    class Config:
        orm_mode = True
