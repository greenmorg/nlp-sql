from pydantic import BaseModel

class EmbeddingSchema(BaseModel):
    name: str
    embeddings: list[float]
    text_schema: str

    class Config:
        orm_mode = True
