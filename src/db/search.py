from enum import Enum
from dataclasses import dataclass, asdict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import DBEmbedding
from src.utils.openai_utils import context_aware_text_to_embedding

class Distance(Enum):
    L1 = "l1_distance"
    L2 = "l2_distance"
    COSINE = "cosine_distance"
    INNER_PRODUCT = "vector_ip_ops"

class Distance(Enum):
    L1 = "l1_distance"
    L2 = "l2_distance"
    COSINE = "cosine_distance"
    INNER_PRODUCT = "vector_ip_ops"

@dataclass
class SearchResult:
    text_schema: str

@dataclass
class EmbeddingSearchResult(SearchResult):
    text_schema: str

@dataclass
class StringSearchResult(SearchResult):
    text_schema: str

class Searcher:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def search(self, query: str, distance: Distance = Distance.COSINE, limit: int = 3) -> list[EmbeddingSearchResult]:
        query_vector = await context_aware_text_to_embedding(query)
        distance_fn = getattr(DBEmbedding.embeddings, distance.value)
        neighbors = await self.db.scalars(
            select(DBEmbedding).order_by(distance_fn(query_vector)).limit(limit)
        )
        res = [EmbeddingSearchResult(text_schema=n.text_schema) for n in neighbors]
        print(res)
        return res
        # return [EmbeddingSearchResult(schema_name=n.name, content=n.embeddings, text_schema=n.text_schema) for n in neighbors]
