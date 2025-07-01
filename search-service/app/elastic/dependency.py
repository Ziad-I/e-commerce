from fastapi import FastAPI, Request


async def get_elasticsearch(request: Request):
    """
    Get the Elasticsearch client from the app state.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        AsyncElasticsearch: The Elasticsearch client.
    """
    yield request.app.state.elasticsearch
