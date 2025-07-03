from functools import lru_cache
from elasticsearch import AsyncElasticsearch
from loguru import logger

from app.core.config import settings


class ElasticClient:
    """
    Singleton class to manage the Elasticsearch client.
    """

    client: AsyncElasticsearch = None

    def __init__(self, hosts: list, user: str, password: str):
        self.hosts = hosts
        self.user = user
        self.password = password

    async def connect(self):
        """
        Establish a connection to the Elasticsearch cluster.
        """
        if not self.client:
            self.client = AsyncElasticsearch(
                hosts=self.hosts,
                basic_auth=(self.user, self.password),
                verify_certs=False,  # Set to True in production
            )
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

        try:
            resp = await self.client.search(index=index, body=body)
            return resp
        except Exception as e:
            logger.error(f"Failed to perform search: {e}")
            raise ValueError(f"Failed to perform search: {e}")

    async def index_product(self, index: str, id: str, document: dict):
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

        try:
            resp = await self.client.index(index=index, id=id, body=document)
            logger.info(f"Document indexed with ID: {id}")
            return resp
        except Exception as e:
            logger.error(f"Failed to index document: {e}")
            raise ValueError(f"Failed to index document: {e}")

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

        try:
            resp = await self.client.delete(index=index, id=id)
            logger.info(f"Document deleted with ID: {id}")
            return resp
        except Exception as e:
            logger.error(f"Failed to delete document with ID {id}: {e}")
            raise ValueError(f"Failed to delete document with ID {id}: {e}")

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

        try:
            resp = await self.client.update(index=index, id=id, body={"doc": document})
            logger.info(f"Document updated with ID: {id}")
            return resp
        except Exception as e:
            logger.error(f"Failed to update document with ID {id}: {e}")
            raise ValueError(f"Failed to update document with ID {id}: {e}")


@lru_cache
def get_elastic_client() -> ElasticClient:
    """
    Get a singleton Elasticsearch client instance.
    """
    return ElasticClient(
        hosts=[settings.ELASTICSEARCH_HOST],
        user=settings.ELASTICSEARCH_USER,
        password=settings.ELASTICSEARCH_PASSWORD,
    )
