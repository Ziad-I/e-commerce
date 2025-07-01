from functools import lru_cache
from elasticsearch import AsyncElasticsearch

from app.core.config import settings


@lru_cache
def get_elastic_client() -> AsyncElasticsearch:
    """
    Get a singleton Elasticsearch client instance.
    """
    return AsyncElasticsearch(
        hosts=[settings.ELASTICSEARCH_HOST],
    )
