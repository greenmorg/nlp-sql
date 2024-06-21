import os
import asyncio
import logging

from sqlalchemy import text
from dotenv import load_dotenv


load_dotenv()


def setup_logging(logger_name: str | None = None) -> logging.Logger:
    """
    Setup the logging for the application.

    Arguments:
        path: str - The path to save the log file.

    Returns:
        logging.Logger - The logger to use.
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logger = logging.getLogger(logger_name)
    logger.addHandler(console)
    return logger

logger = setup_logging()

async def main(): 
    logger.info("Read env vars...")
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")
    logger.info(f"PYTHONPATH = {os.environ.get('PYTHONPATH')}")
    print(host, port, user, password, db_name)
    if not (host and port): raise ValueError("The host and port should not be empty. Check you env file, please!")
    if not user:
        user = "admin"
    if not db_name:
        db_name = "database_schema"
    logger.info("DONE.")
    logger.info("Starting DB initialization...")
    from models import EngineParams, Base
    from vectorized_postgres_engine import get_vectorized_postgres_engine
    from src.utils.tokenizer import EMBEDDING_SHAPE
    engine_params = EngineParams(host=host, port=port, user=user, password=password, db_name=db_name)
    engine = get_vectorized_postgres_engine(engine_params)


    async with engine.begin() as conn:
        logger.info("Enabling the pgvector extension for Postgres...")
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        logger.info("Creating database tables and indexes...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info(f"EMBEDDING_DIM = {EMBEDDING_SHAPE}")
    
    await engine.dispose()
    logger.info("The database was successfuly created")


if __name__ == "__main__":
    asyncio.run(main())