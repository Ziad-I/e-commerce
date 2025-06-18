from fastapi import APIRouter

from app.schemas.user import UserCreate, UserRead
from app.auth.backend import auth_backend_refresh
from app.auth.dependency import fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend_refresh), tags=["Auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["Auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["Auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    tags=["Auth"],
)
