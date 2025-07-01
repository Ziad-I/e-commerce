from pydantic import BaseModel, Field
from typing import List, Optional

from app.models.product import Product


class SearchResponse(BaseModel):
    """
    Response model for search results.

    Attributes:
        total (int): Total number of results found.
        items (List[Product]): List of search result product.
    """

    total: int = Field(..., description="Total number of results found")
    items: List[Product] = Field(..., description="List of search result items")
