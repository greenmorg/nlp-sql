from sqlalchemy import Engine, event
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from pydantic import BaseModel

class EngineParams(BaseModel):
    host: str
    port: int
    user: str
    password: str
    db_name: str

def get_vectorized_postgres_engine(params: EngineParams) -> AsyncEngine:
    DATABASE_URI = f"postgresql+asyncpg://{params.user}:{params.password}@{params.host}:{params.port}/{params.db_name}"
    return create_async_engine(url=DATABASE_URI)

