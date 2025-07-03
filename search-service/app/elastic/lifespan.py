from loguru import logger
from fastapi import FastAPI

from app.elastic.elastic import get_elastic_client
from app.core.config import settings


async def init_elasticsearch(app: FastAPI):
    """
    Initialize the Elasticsearch client.
    """
    es = get_elastic_client()
    app.state.elasticsearch = es
    await es.connect()
    logger.info("Elasticsearch client initialized and connected.")


async def close_elasticsearch(app: FastAPI):
    """
    Close the Elasticsearch client.
    """
    if hasattr(app.state, "elasticsearch"):
        await app.state.elasticsearch.close()
    logger.info("Elasticsearch client closed.")
