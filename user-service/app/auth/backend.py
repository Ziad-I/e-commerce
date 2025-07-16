from typing import Generic
from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi_users.authentication import AuthenticationBackend
from fastapi_users.types import DependencyCallable
from fastapi_users import models
from fastapi_users.authentication.strategy import (
    Strategy,
    StrategyDestroyNotSupportedError,
)
from fastapi_users.authentication.transport import (
    Transport,
    TransportLogoutNotSupportedError,
)

from app.auth.transport import BearerTransportRefresh, CookieTransportRefresh
from app.auth.strategy import get_jwt_strategy, get_refresh_jwt_strategy
from app.core.config import settings


class AuthenticationBackendRefresh(
    AuthenticationBackend, Generic[models.UP, models.ID]
):

    def __init__(
        self,
        name: str,
        transport: Transport,
        get_strategy: DependencyCallable[Strategy[models.UP, models.ID]],
        get_refresh_strategy: DependencyCallable[Strategy[models.UP, models.ID]],
    ):
        self.name = name
        self.transport = transport
        self.get_strategy = get_strategy
        self.get_refresh_strategy = get_refresh_strategy

    async def login(
        self,
        strategy: Strategy[models.UP, models.ID],
        refresh_strategy: Strategy[models.UP, models.ID],
        user: models.UP,
    ) -> Response:
        token = await strategy.write_token(user)
        refresh_token = await refresh_strategy.write_token(user)

        response: JSONResponse = await self.transport.get_login_response(
            token=token, refresh_token=refresh_token
        )
        return response

    async def logout(
        self,
        strategy: Strategy[models.UP, models.ID],
        refresh_strategy: Strategy[models.UP, models.ID],
        user: models.UP,
        token: str,
        refresh_token: str | None = None,
    ) -> Response:
        try:
            await strategy.destroy_token(token, user)
            await refresh_strategy.destroy_token(refresh_token, user)
        except StrategyDestroyNotSupportedError:
            pass

        try:
            response = await self.transport.get_logout_response()
        except TransportLogoutNotSupportedError:
            response = Response(status_code=status.HTTP_204_NO_CONTENT)
            response.delete_cookie("refresh_token")

        return response

    async def refresh(
        self,
        strategy: Strategy[models.UP, models.ID],
        refresh_strategy: Strategy[models.UP, models.ID],
        user: models.UP,
        user_token: str,
        refresh_token: str,
    ) -> Response:
        try:
            await strategy.destroy_token(user_token, user)
            await refresh_strategy.destroy_token(refresh_token, user)
        except StrategyDestroyNotSupportedError:
            pass

        new_token = await strategy.write_token(user)
        new_refresh_token = await refresh_strategy.write_token(user)

        response: JSONResponse = await self.transport.get_login_response(
            token=new_token, refresh_token=new_refresh_token
        )
        return response


bearer_transport_refresh = BearerTransportRefresh(
    tokenUrl=f"{settings.API_V1_STR}/users/auth/jwt/login"
)

cookie_transport_refresh = CookieTransportRefresh(
    cookie_name="access_token",
    refresh_cookie_name="refresh_token",
    cookie_max_age=settings.ACCESS_TOKEN_LIFETIME_SECONDS,
    refresh_cookie_max_age=settings.REFRESH_TOKEN_LIFETIME_SECONDS,
)

jwt_authentication_backend = AuthenticationBackendRefresh(
    name="jwt",
    transport=bearer_transport_refresh,
    get_strategy=get_jwt_strategy,
    get_refresh_strategy=get_refresh_jwt_strategy,
)

cookie_authentication_backend = AuthenticationBackendRefresh(
    name="cookie",
    transport=cookie_transport_refresh,
    get_strategy=get_jwt_strategy,
    get_refresh_strategy=get_refresh_jwt_strategy,
)
