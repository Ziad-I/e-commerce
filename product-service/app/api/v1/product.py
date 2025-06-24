from fastapi import APIRouter, HTTPException
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.crud import product as product_crud

router = APIRouter()


@router.get("/", response_model=list[ProductRead], summary="Get all products")
async def get_all_products(skip: int = 0, limit: int = 100):
    """
    Retrieve all products with pagination.

    - **skip**: Number of products to skip (default is 0).
    - **limit**: Maximum number of products to return (default is 100).
    """
    products = await product_crud.get_all_products(skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=ProductRead, summary="Get product by ID")
async def get_product_by_id(product_id: str):
    """
    Retrieve a product by its ID.

    - **product_id**: The ID of the product to retrieve.
    """
    product = await product_crud.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductRead, summary="Create a new product")
async def create_product(product: ProductCreate):
    """
    Create a new product.

    - **product**: The product data to create.
    """
    new_product = await product_crud.create_product(product)
    return new_product


@router.put("/{product_id}", response_model=ProductRead, summary="Update a product")
async def update_product(product_id: str, product: ProductUpdate):
    """
    Update an existing product.

    - **product_id**: The ID of the product to update.
    - **product**: The updated product data.
    """
    updated_product = await product_crud.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/{product_id}", response_model=ProductRead, summary="Delete a product")
async def delete_product(product_id: str):
    """
    Delete a product by its ID.

    - **product_id**: The ID of the product to delete.
    """
    deleted_product = await product_crud.delete_product(product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product


@router.get(
    "/category/{category}",
    response_model=list[ProductRead],
    summary="Get products by category",
)
async def get_products_by_category(category: str, skip: int = 0, limit: int = 100):
    """
    Retrieve products by category with pagination.

    - **category**: The category of products to retrieve.
    - **skip**: Number of products to skip (default is 0).
    - **limit**: Maximum number of products to return (default is 100).
    """
    products = await product_crud.get_products_by_category(
        category, skip=skip, limit=limit
    )
    return products
