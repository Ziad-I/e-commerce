from typing import List
from fastapi import APIRouter, HTTPException, status, Response

from app.schemas.cart import (
    CartRead,
    CartUpdate,
    CartItemCreate,
    CartItemUpdate,
)
from app.crud import cart as crud_cart

router = APIRouter()


@router.get("/{user_id}")
async def get_cart(user_id: str) -> CartRead:
    """Get the cart for a specific user."""
    cart = await crud_cart.get_or_create_cart(user_id)
    return cart


@router.post("/{user_id}/items")
async def add_item(user_id: str, item: CartItemCreate) -> CartRead:
    """Add an item to the user's cart."""
    try:
        cart = await crud_cart.add_item_to_cart(
            user_id=user_id,
            product_id=item.product_id,
            product_name=item.product_name,
            quantity=item.quantity,
        )
        return cart
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{user_id}/items/{product_id}")
async def update_item(
    user_id: str, product_id: str, update: CartItemUpdate
) -> CartRead:
    """Update the quantity of an item in the cart."""
    cart = await crud_cart.update_item_quantity(
        user_id=user_id, product_id=product_id, new_quantity=update.quantity
    )

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found in cart",
        )
    return cart


@router.delete("/{user_id}/items/{product_id}")
async def remove_item(user_id: str, product_id: str) -> CartRead:
    """Remove an item from the cart."""
    cart = await crud_cart.remove_item_from_cart(user_id=user_id, product_id=product_id)

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found in cart",
        )

    return cart


@router.delete("/{user_id}/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear_user_cart(user_id: str):
    """Clear all items from the user's cart."""
    await crud_cart.clear_cart(user_id)
    return


@router.post("/{user_id}/refresh-prices")
async def refresh_prices(user_id: str) -> CartRead:
    """Refresh all prices in the cart from the pricing service."""
    cart = await crud_cart.refresh_cart(user_id)
    return cart
