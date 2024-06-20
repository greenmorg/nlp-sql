from pydantic import BaseModel

class EmbeddingSchema(BaseModel):
    name: str
    embeddings: list[int]

    class Config:
        orm_mode = True
