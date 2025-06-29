from typing import Optional, List
from pydantic import Field
from beanie import Document, PydanticObjectId


class Product(Document):
    name: str = Field(..., description="Name of the product")
    description: Optional[str] = Field(..., description="Description of the product")
    price: float = Field(..., description="Price of the product")
    category: Optional[str] = Field(..., description="Category of the product")
    tags: Optional[List[str]] = Field(
        default_factory=list, description="List of tags associated with the product"
    )
    quantity: int = Field(..., description="Available quantity of the product")
    images: Optional[List[str]] = Field(
        default_factory=list, description="List of image URLs for the product"
    )

    class Config:
        json_encoders = {PydanticObjectId: str}
