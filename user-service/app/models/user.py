from datetime import datetime
from typing import List
from beanie import Document, Link, BackLink, PydanticObjectId
from pydantic import Field, model_validator
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase


class User(BeanieBaseUser, Document):
    # name: str = Field(..., description="The user's full name")
    # surname: str = Field(..., description="The user's surname")
    # phone: str = Field(..., description="The user's phone number")

    # created_at: datetime = Field(
    #     default_factory=datetime.now, description="Creation timestamp"
    # )
    # updated_at: datetime = Field(
    #     default_factory=datetime.now, description="Last update timestamp"
    # )

    # @model_validator(mode="after")
    # def update_timestamp(cls, values):
    #     values["updated_at"] = datetime.now()
    #     return values

    class Config:
        json_encoders = {PydanticObjectId: str}
