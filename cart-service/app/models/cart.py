from typing import Annotated, Optional, List
from pydantic import BaseModel, Field
from beanie import Document, Indexed


class CartItem(BaseModel):
    product_id: str = Field(..., description="ID of the product")
    product_name: str = Field(..., description="Name of the product")
    quantity: int = Field(..., ge=1, description="Quantity of the product in the cart")
    price: float = Field(..., ge=0, description="Price of the product")


class Cart(Document):
    user_id: Annotated[int, Indexed(unique=True)] = Field(
        ..., description="ID of the user who owns the cart"
    )
    items: List[CartItem] = Field(
        default_factory=list, description="List of items in the cart"
    )
    total_price: float = Field(
        default=0.0, ge=0, description="Total price of all items in the cart"
    )

    def calculate_total_price(self):
        """Calculate the total price of all items in the cart."""
        self.total_price = sum(item.price * item.quantity for item in self.items)
