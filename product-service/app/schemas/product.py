from typing import Optional, List
from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class ProductCreate(BaseModel):
    """Schema for creating a new product"""

    name: str = Field(
        ..., description="Name of the product", min_length=1, max_length=255
    )
    description: Optional[str] = Field(
        None, description="Description of the product", max_length=1000
    )
    price: float = Field(..., description="Price of the product", gt=0)
    category: Optional[str] = Field(
        None, description="Category of the product", max_length=100
    )
    tags: Optional[List[str]] = Field(
        default_factory=list, description="List of tags associated with the product"
    )
    quantity: int = Field(..., description="Available quantity of the product", ge=0)
    images: Optional[List[str]] = Field(
        default_factory=list, description="List of image URLs for the product"
    )


class ProductUpdate(BaseModel):
    """Schema for updating an existing product"""

    name: Optional[str] = Field(
        None, description="Name of the product", min_length=1, max_length=255
    )
    description: Optional[str] = Field(
        None, description="Description of the product", max_length=1000
    )
    price: Optional[float] = Field(None, description="Price of the product", gt=0)
    category: Optional[str] = Field(
        None, description="Category of the product", max_length=100
    )
    tags: Optional[List[str]] = Field(
        None, description="List of tags associated with the product"
    )
    quantity: Optional[int] = Field(
        None, description="Available quantity of the product", ge=0
    )
    images: Optional[List[str]] = Field(
        None, description="List of image URLs for the product"
    )


class ProductRead(BaseModel):
    """Schema for reading/returning product data"""

    id: PydanticObjectId = Field(..., description="Unique identifier of the product")
    name: str = Field(..., description="Name of the product")
    description: Optional[str] = Field(None, description="Description of the product")
    price: float = Field(..., description="Price of the product")
    category: Optional[str] = Field(None, description="Category of the product")
    tags: List[str] = Field(
        default_factory=list, description="List of tags associated with the product"
    )
    quantity: int = Field(..., description="Available quantity of the product")
    images: List[str] = Field(
        default_factory=list, description="List of image URLs for the product"
    )

    class Config:
        json_encoders = {PydanticObjectId: str}
        from_attributes = True


class ProductDelete(BaseModel):
    """Schema for deleting a product"""

    id: PydanticObjectId = Field(
        ..., description="Unique identifier of the product to delete"
    )

    class Config:
        json_encoders = {PydanticObjectId: str}


class ProductList(BaseModel):
    """Schema for listing products with pagination"""

    limit: int = Field(..., description="Number of products per page")
    skip: int = Field(0, description="Number of products to skip for pagination")


class ProductListResponse(BaseModel):
    """Schema for the response of a product list"""

    products: List[ProductRead] = Field(
        default_factory=list, description="List of products"
    )
    total: int = Field(..., description="Total number of products")
    pages: int = Field(..., description="Total number of pages based on the limit")

    class Config:
        json_encoders = {PydanticObjectId: str}
        from_attributes = True
