from fastapi import APIRouter

from app.api.v1 import cart

v1_router = APIRouter()
v1_router.include_router(cart.router, prefix="/cart", tags=["cart"])
