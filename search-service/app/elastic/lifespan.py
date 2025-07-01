from app.elastic.elastic import get_elastic_client
from fastapi import FastAPI

from app.core.config import settings


async def init_elasticsearch(app: FastAPI):
    """
    Initialize the Elasticsearch client.
    """
    app.state.elasticsearch = get_elastic_client()


async def close_elasticsearch(app: FastAPI):
    """
    Close the Elasticsearch client.
    """
    if hasattr(app.state, "elasticsearch"):
        await app.state.elasticsearch.close()
