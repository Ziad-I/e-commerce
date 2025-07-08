from pydantic import BaseModel, Field
from typing import List, Optional


class CartItem(BaseModel):
    product_id: str
    product_name: str
    price: float
    quantity: int


class CartRead(BaseModel):
    user_id: str
    items: List[CartItem] = []
    total_price: Optional[float] = 0.0


class CartCreate(BaseModel):
    user_id: str


class CartUpdate(BaseModel):
    items: List[CartItem]


class CartItemCreate(BaseModel):
    product_id: str
    product_name: str
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: int
