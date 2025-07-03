from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.config import settings
from app.elastic.dependency import get_elasticsearch
from app.elastic.elastic import ElasticClient
from app.schemas.search import SearchResponse

router = APIRouter()


@router.get("/")
async def search(
    q: Optional[str] = Query(None, description="Full-text search query"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    category: Optional[str] = Query(None, description="Filter by category"),
    sort: Optional[str] = Query(
        None,
        description="Sort directive, e.g. 'price:asc', 'name:desc'; defaults to '_score:desc'",
    ),
    limit: int = Query(10, gt=0, le=100, description="Max number of results to return"),
    skip: int = Query(0, ge=0, description="Number of items to skip for pagination"),
    es: ElasticClient = Depends(get_elasticsearch),
) -> SearchResponse:
    """
    Search endpoint to query the search service.

    Args:
        q (Optional[str]): Full-text search query.
        min_price (Optional[float]): Minimum price filter.
        max_price (Optional[float]): Maximum price filter.
        category (Optional[str]): Category filter.
        sort (Optional[str]): Sort results by field.
        limit (int): Maximum number of results to return.
        skip (int): Number of items to skip for pagination.

    Returns:
        SearchResponse: Response containing total results and items.
    """
    if not q and not min_price and not max_price and not category:
        raise HTTPException(
            status_code=400, detail="At least one filter must be provided"
        )

    query = {"bool": {"must": [], "filter": []}}
    if q:
        query["bool"]["must"].append(
            {"multi_match": {"query": q, "fields": ["name^2", "description"]}}
        )

    if min_price is not None or max_price is not None:
        price_range = {}
        if min_price is not None:
            price_range["gte"] = min_price
        if max_price is not None:
            price_range["lte"] = max_price
        query["bool"]["filter"].append({"range": {"price": price_range}})

    if category:
        query["bool"]["filter"].append({"term": {"category": category}})

    raw_sort = sort or "_score:desc"
    field, sep, direction = raw_sort.partition(":")
    direction = direction if direction in ("asc", "desc") else "desc"
    if field in ["name"]:
        field = f"{field}.keyword"

    sort_field = field if field else "_score"
    search_body = {
        "query": query,
        "sort": [{sort_field: {"order": direction}}],
        "from": skip,
        "size": limit,
    }
    try:
        response = await es.search(
            index=settings.ELASTICSEARCH_INDEX,
            body=search_body,
        )
        total_results = response["hits"]["total"]["value"]
        items = response["hits"]["hits"]

        return SearchResponse(total=total_results, items=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
