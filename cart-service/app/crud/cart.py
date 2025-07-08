from typing import List, Optional

from app.models.cart import Cart, CartItem
from app.schemas.cart import (
    CartCreate,
    CartUpdate,
    CartItemCreate,
    CartItemUpdate,
)
from app.core.grpc_client import get_grpc_client


async def get_or_create_cart(user_id: str) -> Cart:
    """
    Get a cart by user_id, or create a new one if it doesn't exist.
    """
    cart = await Cart.find_one(Cart.user_id == user_id)
    if not cart:
        cart = await Cart(user_id=user_id).insert()
    return cart


async def delete_cart(user_id: str) -> bool:
    cart = await get_or_create_cart(user_id)
    await cart.delete()
    return True


async def add_item_to_cart(
    user_id: str, product_id: str, product_name: str, quantity: int
) -> Optional[Cart]:
    cart = await get_or_create_cart(user_id)

    grpc_client = get_grpc_client()
    price = await grpc_client.get_price(product_id)

    if price is None:
        raise ValueError(f"Could not fetch price for product {product_id}")

    existing_item = next(
        (item for item in cart.items if product_id == product_id), None
    )

    if existing_item:
        existing_item.quantity += quantity
        existing_item.price = price
    else:
        new_item = CartItem(
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            price=price,
        )
        cart.items.append(new_item)
    cart.calculate_total_price()
    await cart.save()
    return cart


async def remove_item_from_cart(user_id: str, product_id: str) -> Optional[Cart]:
    cart = await get_or_create_cart(user_id)

    initial_items_count = len(cart.items)
    cart.items = [item for item in cart.items if item.product_id != product_id]

    if len(cart.items) == initial_items_count:
        return None  # Item not found

    cart.calculate_total_price()
    await cart.save()
    return cart


async def update_item_quantity(
    user_id: str, product_id: str, new_quantity: int
) -> Optional[Cart]:
    cart = await get_or_create_cart(user_id)

    item = next((item for item in cart.items if item.product_id == product_id), None)

    if not item:
        return None

    grpc_client = get_grpc_client()
    price = await grpc_client.get_price(product_id)
    if price is not None:
        item.price = price

    item.quantity = new_quantity
    cart.calculate_total_price()
    await cart.save()
    return cart


async def clear_cart(user_id: str) -> Cart:
    """Clear all items from the user's cart."""
    cart = await get_or_create_cart(user_id)
    cart.items = []
    cart.total_price = 0.0
    await cart.save()
    return cart


async def refresh_cart(user_id: str) -> Optional[Cart]:
    """
    Refresh the cart by recalculating the total price and updating item prices.
    """
    cart = await get_or_create_cart(user_id)

    grpc_client = get_grpc_client()
    for item in cart.items:
        price = await grpc_client.get_price(item.product_id)
        if price is not None:
            item.price = price

    cart.calculate_total_price()
    await cart.save()
    return cart
