from typing import Optional, List
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


async def get_all_products(skip: int, limit: int) -> List[Product]:
    """Retrieve all products from the database."""
    products = await Product.find_all(limit=limit, skip=skip).to_list()
    return products


async def get_products_by_category(
    category: str, skip: int, limit: int
) -> List[Product]:
    """Retrieve products by category from the database."""
    products = await Product.find_all(
        Product.category == category, limit=limit, skip=skip
    ).to_list()
    return products


async def get_product_by_id(product_id: str) -> Optional[Product]:
    """Retrieve a product by its ID from the database."""
    product = await Product.get(product_id)
    if not product:
        return None
    return product


async def create_product(product: ProductCreate) -> Product:
    """Create a new product in the database."""
    new_product = Product(**product.model_dump())
    await new_product.save()
    return new_product


async def update_product(product_id: str, product: ProductUpdate) -> Optional[Product]:
    """Update an existing product in the database."""
    existing_product = await Product.get(product_id)
    if not existing_product:
        return None

    for key, value in product.model_dump().items():
        setattr(existing_product, key, value)

    await existing_product.save()
    return existing_product


async def delete_product(product_id: str) -> Optional[Product]:
    """Delete a product from the database."""
    existing_product = await Product.get(product_id)
    if not existing_product:
        return None

    await existing_product.delete()
    return existing_product
