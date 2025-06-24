from fastapi import APIRouter
from app.api.v1 import product

v1_router = APIRouter()
v1_router.include_router(product.router, prefix="/products", tags=["Products"])
