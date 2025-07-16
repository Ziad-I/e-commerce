from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.auth.backend import jwt_authentication_backend, cookie_authentication_backend
from app.auth.dependency import fastapi_users, current_active_user

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(jwt_authentication_backend),
    prefix="/jwt",
    tags=["Auth"],
)
router.include_router(
    fastapi_users.get_auth_router(cookie_authentication_backend),
    prefix="/cookie",
    tags=["Auth"],
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


@router.post("/validate", tags=["Auth"])
async def validate_user(user: User = Depends(current_active_user)) -> UserRead:
    """Endpoint to validate the current active user."""
    return user
