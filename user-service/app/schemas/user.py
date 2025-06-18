from pydantic import BaseModel
from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import Field


class BaseUserSchema(BaseModel):
    name: str = Field(..., description="The user's full name")
    surname: str = Field(..., description="The user's surname")
    phone: str = Field(..., description="The user's phone number")


class UserRead(schemas.BaseUser[PydanticObjectId], BaseUserSchema):
    pass


class UserCreate(schemas.BaseUserCreate, BaseUserSchema):
    pass


class UserCreate(schemas.BaseUserCreate, BaseUserSchema):
    pass


class UserUpdate(schemas.BaseUserUpdate, BaseUserSchema):
    pass
