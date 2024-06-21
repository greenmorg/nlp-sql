from enum import Enum
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import DBEmbedding

from src.utils.types import embedding
from src.utils.tokenizer import text_to_embedding, embedding_to_text

class Distance(Enum):
    L1 = "l1_distance"
    L2 = "l2_distance"
    COSINE = "cosine_distance"
    INNER_PRODUCT = "vector_ip_ops"

@dataclass
class SearchResult:
    schema_name: str
    content: str | embedding

@dataclass
class EmbeddingSearchResult(SearchResult):
    content: embedding

    def to_string_result(self): 
        return StringSearchResult(schema_name=self.schema_name, 
                                  content=embedding_to_text(self.content)) 
    
@dataclass
class StringSearchResult(SearchResult):
    content: str

    def to_embedding_result(self): 
        return EmbeddingSearchResult(schema_name=self.schema_name, 
                                     content=text_to_embedding(self.content))
    

class Searcher:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search(self, query: str, distance: Distance = Distance.COSINE, limit: int = 5) -> list[EmbeddingSearchResult]:
        query_tokens = text_to_embedding(query)
        distance_fn = getattr(DBEmbedding.embeddings, distance.value)
        neighbors = await self.db.scalars(
            select(DBEmbedding).order_by(distance_fn(query_tokens)).limit(limit)
        )
        return [EmbeddingSearchResult(schema_name=n.name, content=n.embeddings.astype(int).tolist()) for n in neighbors]
            
