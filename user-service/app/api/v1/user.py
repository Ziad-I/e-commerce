from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import UserRead, UserUpdate
from app.auth.dependency import fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    tags=["Users"],
)
