from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.user import router as user_router

v1_router = APIRouter()
v1_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
v1_router.include_router(user_router, prefix="/users", tags=["Users"])
