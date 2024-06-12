import os
import asyncio
import logging

from sqlalchemy import text
from dotenv import load_dotenv

from models import *
from vectorized_postgres_engine import *

load_dotenv()

logger = logging.getLogger()

async def main(): 
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")
    db_name = os.environ.get("DB_NAME")
    if not (host and port): raise ValueError("The host and port should not be empty. Check you env file, please!")
    if not user:
        user = "admin"
    if not db_name:
        db_name = "database_schema"
    engine_params = EngineParams(host=host, port=port, user=user, password=password, db_name=db_name)
    engine = get_vectorized_postgres_engine(engine_params)

    async with engine.begin() as conn:
        logger.info("Enabling the pgvector extension for Postgres...")
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        logger.info("Creating database tables and indexes...")
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(main())