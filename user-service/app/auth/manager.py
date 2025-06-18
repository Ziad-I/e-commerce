from typing import Optional
from loguru import logger
from beanie import PydanticObjectId
from fastapi import Request
from fastapi_users import BaseUserManager
from fastapi_users.db import ObjectIDIDMixin

from app.core.config import settings
from app.models.user import User


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_reset_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has reset their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )

    async def on_after_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has been verified. Verification token: {token}")
