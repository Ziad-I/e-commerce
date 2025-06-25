from aio_pika import Channel
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from redis.asyncio import Redis

from app.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.crud import product as product_crud

from app.redis.dependency import get_redis
from app.redis.cache import set_product_cache, get_product_cache, delete_product_cache
from app.rabbitmq.dependency import get_rabbit_channel
from app.rabbitmq.publisher import publish_message

router = APIRouter()


@router.get("/", summary="Get all products")
async def get_all_products(skip: int = 0, limit: int = 100) -> list[ProductRead]:
    """
    Retrieve all products with pagination.

    - **skip**: Number of products to skip (default is 0).
    - **limit**: Maximum number of products to return (default is 100).
    """
    products = await product_crud.get_all_products(skip=skip, limit=limit)
    return products


@router.get("/{product_id}", summary="Get product by ID")
async def get_product_by_id(
    product_id: str,
    background_tasks: BackgroundTasks,
    redis: Redis = Depends(get_redis),
) -> ProductRead:
    """
    Retrieve a product by its ID.

    - **product_id**: The ID of the product to retrieve.
    """
    cached_product = await get_product_cache(redis, product_id)
    if cached_product:
        return ProductRead.model_validate_json(cached_product)

    product = await product_crud.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    background_tasks.add_task(
        set_product_cache, redis, product_id, product.model_dump_json()
    )
    return product


@router.post("/", summary="Create a new product")
async def create_product(
    product: ProductCreate,
    background_tasks: BackgroundTasks,
    redis: Redis = Depends(get_redis),
    rabbit_channel: Channel = Depends(get_rabbit_channel),
) -> ProductRead:
    """
    Create a new product.

    - **product**: The product data to create.
    """
    new_product = await product_crud.create_product(product)

    background_tasks.add_task(
        set_product_cache, redis, new_product.id, new_product.model_dump_json()
    )
    background_tasks.add_task(
        publish_message,
        rabbit_channel,
        "product.created",
        new_product.model_dump_json(),
    )

    return new_product


@router.put("/{product_id}", summary="Update a product")
async def update_product(
    product_id: str,
    product: ProductUpdate,
    background_tasks: BackgroundTasks,
    redis: Redis = Depends(get_redis),
    rabbit: Channel = Depends(get_rabbit_channel),
) -> ProductRead:
    """
    Update an existing product.

    - **product_id**: The ID of the product to update.
    - **product**: The updated product data.
    """
    updated_product = await product_crud.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")

    background_tasks.add_task(
        set_product_cache, redis, product_id, updated_product.model_dump_json()
    )
    background_tasks.add_task(
        publish_message,
        rabbit,
        "product.updated",
        updated_product.model_dump_json(),
    )
    return updated_product


@router.delete("/{product_id}", summary="Delete a product")
async def delete_product(
    product_id: str,
    background_tasks: BackgroundTasks,
    redis: Redis = Depends(get_redis),
    rabbit: Channel = Depends(get_rabbit_channel),
) -> ProductRead:
    """
    Delete a product by its ID.

    - **product_id**: The ID of the product to delete.
    """
    deleted_product = await product_crud.delete_product(product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")

    background_tasks.add_task(delete_product_cache, redis, product_id)
    background_tasks.add_task(
        publish_message,
        rabbit,
        "product.deleted",
        deleted_product.model_dump_json(),
    )
    return deleted_product


@router.get("/category/{category}", summary="Get products by category")
async def get_products_by_category(
    category: str, skip: int = 0, limit: int = 100
) -> list[ProductRead]:
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
