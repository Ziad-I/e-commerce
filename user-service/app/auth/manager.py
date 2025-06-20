import asyncio
from typing import Optional
from loguru import logger
from beanie import PydanticObjectId
from fastapi import Request
from fastapi_users import BaseUserManager
from fastapi_users.db import ObjectIDIDMixin

from app.core.config import settings
from app.models.user import User
from app.core.grpc_client import get_grpc_client
from app.proto import notification_pb2


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    reset_password_token_lifetime_seconds = (
        settings.RESET_PASSWORD_TOKEN_LIFETIME_SECONDS
    )
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET
    verification_token_lifetime_seconds = settings.VERIFICATION_TOKEN_LIFETIME_SECONDS

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has requested a password reset. sending email…")
        try:
            email_req = notification_pb2.SendEmailRequest(
                to=user.email,
                type=notification_pb2.EmailType.EMAIL_TYPE_PASSWORD_RESET,
                metadata={
                    "link": settings.FRONTEND_URL + f"/reset-password?token={token}",
                    "lifetime": "1 hour",
                },
            )
            asyncio.create_task(get_grpc_client().send_email(email_req))
        except Exception as e:
            logger.error(f"Failed to send password reset email: {e}")

    async def on_after_reset_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has reset their password.")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has requested email verification. sending email…")
        try:
            email_req = notification_pb2.SendEmailRequest(
                to=user.email,
                type=notification_pb2.EmailType.EMAIL_TYPE_VERIFY,
                metadata={
                    "link": settings.FRONTEND_URL + f"/verify-email?token={token}",
                    "lifetime": "24 hours",
                },
            )
            asyncio.create_task(get_grpc_client().send_email(email_req))
        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")

    async def on_after_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has been verified.")
