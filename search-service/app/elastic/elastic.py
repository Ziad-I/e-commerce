from functools import lru_cache
from elasticsearch import AsyncElasticsearch

from app.core.config import settings


class ElasticClient:
    """
    Singleton class to manage the Elasticsearch client.
    """

    client: AsyncElasticsearch = None

    def __init__(self, hosts: list = None):
        self.hosts = hosts

    async def connect(self):
        """
        Establish a connection to the Elasticsearch cluster.
        """
        if not self.client:
            self.client = AsyncElasticsearch(hosts=self.hosts)
            try:
                await self.client.info()
            except Exception as e:
                raise ConnectionError(f"Failed to connect to Elasticsearch: {e}")

    async def close(self):
        """
        Close the Elasticsearch client connection.
        """
        if self.client:
            await self.client.close()
            self.client = None

    async def search(self, index: str, body: dict):
        """
        Perform a search query on the specified index.

        Args:
            index (str): The Elasticsearch index to search.
            body (dict): The search query body.

        Returns:
            dict: The search results.
        """
        if not self.client:
            raise ValueError("Elasticsearch client is not initialized.")

        resp = await self.client.search(index=index, body=body)
        return resp

    async def index_product(self, index: str, document: dict):
        """
        Index a product document.

        Args:
            index (str): The Elasticsearch index to use.
            document (dict): The product document to index.

        Returns:
            dict: The response from the indexing operation.
        """
        if not self.client:
            raise ValueError("Elasticsearch client is not initialized.")

        resp = await self.client.index(index=index, body=document)
        return resp

    async def delete_product(self, index: str, id: str):
        """
        Delete a product document by ID.

        Args:
            index (str): The Elasticsearch index to use.
            id (str): The ID of the product document to delete.

        Returns:
            dict: The response from the deletion operation.
        """
        if not self.client:
            raise ValueError("Elasticsearch client is not initialized.")

        resp = await self.client.delete(index=index, id=id)
        return resp

    async def update_product(self, index: str, id: str, document: dict):
        """
        Update a product document by ID.

        Args:
            index (str): The Elasticsearch index to use.
            id (str): The ID of the product document to update.
            document (dict): The updated product document.

        Returns:
            dict: The response from the update operation.
        """
        if not self.client:
            raise ValueError("Elasticsearch client is not initialized.")

        resp = await self.client.update(index=index, id=id, body={"doc": document})
        return resp


@lru_cache
def get_elastic_client() -> ElasticClient:
    """
    Get a singleton Elasticsearch client instance.
    """
    return ElasticClient(hosts=[settings.ELASTICSEARCH_HOST])
