from datetime import datetime
from typing import List
from beanie import Document, PydanticObjectId, after_event, Replace, Update
from pydantic import Field, model_validator
from fastapi_users.db import BeanieBaseUser


class User(BeanieBaseUser, Document):
    name: str = Field(..., description="The user's full name")
    surname: str = Field(..., description="The user's surname")
    phone: str = Field(..., description="The user's phone number")

    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )

    @after_event(Replace, Update)
    def update_timestamp(self):
        self.updated_at = datetime.now()

    class Config:
        json_encoders = {PydanticObjectId: str}
