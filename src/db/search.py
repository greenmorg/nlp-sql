from enum import Enum
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine

from .models import DBEmbedding

from utils.types import embedding
from utils.tokenizer import encode, decode, per_byte_decoding

class Distance(Enum):
    L1 = "l1_distance"
    L2 = "l2_distance"
    COSINE = "cosine_distance"
    INNER_PRODUCT = "vector_ip_ops"

@dataclass
class SearchResult:
    pass

@dataclass
class EmbeddingSearchResult(SearchResult):
    content: embedding

    def to_string_result(self): return StringSearchResult(content=decode(self.content)) 
    
@dataclass
class StringSearchResult(SearchResult):
    content: str

    def to_embedding_result(self): return EmbeddingSearchResult(content=encode(self.content))
    

class Searcher:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def search(self, query: str, distance: Distance = Distance.COSINE, limit: int = 5) -> list[EmbeddingSearchResult]:
        query_tokens = encode(query)
        distance_fn = getattr(DBEmbedding.embeddings, distance)
        async with self.engine.connect() as session:
            neighbors = await session.scalars(
                select(DBEmbedding).order_by(distance_fn(query_tokens)).limit(limit)
                )
        return [EmbeddingSearchResult(content=n) for n in neighbors]
            
