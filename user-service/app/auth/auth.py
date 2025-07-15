from typing import Annotated, Generic, Tuple
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, FastAPIUsers, models
from fastapi_users.authentication import Strategy
from fastapi_users.authentication import Authenticator
from fastapi_users.authentication.strategy import StrategyDestroyNotSupportedError
from fastapi_users.manager import UserManagerDependency
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorModel

from app.auth.error import ErrorCode
from app.auth.backend import AuthenticationBackendRefresh


def get_auth_refresh_router(
    backend: AuthenticationBackendRefresh[models.UP, models.ID],
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    authenticator: Authenticator[models.UP, models.ID],
    requires_verification: bool = False,
) -> APIRouter:
    """
    Generate a router with login/logout/refresh routes for an authentication backend.

    :param backend: The authentication backend instance.
    :param get_user_manager: Dependency callable to get the user manager.
    :param authenticator: The authenticator instance.
    :param requires_verification: Whether the authentication
        requires the user to be verified or not. Defaults to False.
    """
    router = APIRouter()
    get_current_user_token = authenticator.current_user_token(
        active=True, verified=requires_verification
    )

    login_responses: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.LOGIN_BAD_CREDENTIALS: {
                            "summary": "Bad credentials or the user is inactive.",
                            "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
                        },
                        ErrorCode.LOGIN_USER_NOT_VERIFIED: {
                            "summary": "The user is not verified.",
                            "value": {"detail": ErrorCode.LOGIN_USER_NOT_VERIFIED},
                        },
                    }
                }
            },
        },
        **backend.transport.get_openapi_login_responses_success(),
    }

    @router.post(
        "/login",
        name=f"auth:{backend.name}.login",
        responses=login_responses,
    )
    async def login(
        request: Request,
        credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_manager: Annotated[
            BaseUserManager[models.UP, models.ID], Depends(get_user_manager)
        ],
        strategy: Annotated[
            Strategy[models.UP, models.ID], Depends(backend.get_strategy)
        ],
        refresh_strategy: Annotated[
            Strategy[models.UP, models.ID], Depends(backend.get_refresh_strategy)
        ],
    ):
        user = await user_manager.authenticate(credentials)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )
        if requires_verification and not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
            )
        response = await backend.login(strategy, refresh_strategy, user)

        await user_manager.on_after_login(user, request, response)
        return response

    logout_responses: OpenAPIResponseType = {
        **{
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user."
            }
        },
        **backend.transport.get_openapi_logout_responses_success(),
    }

    @router.post(
        "/logout", name=f"auth:{backend.name}.logout", responses=logout_responses
    )
    async def logout(
        user_token: Annotated[Tuple[models.UP, str], Depends(get_current_user_token)],
        strategy: Annotated[
            Strategy[models.UP, models.ID], Depends(backend.get_strategy)
        ],
        refresh_strategy: Annotated[
            Strategy[models.UP, models.ID], Depends(backend.get_refresh_strategy)
        ],
        refresh_token: Annotated[str | None, Cookie()],
    ):
        user, token = user_token
        return await backend.logout(
            strategy,
            refresh_strategy,
            user,
            token,
            refresh_token,
        )

    refresh_responses: OpenAPIResponseType = {
        **{
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing or invalid refresh token."
            },
        },
        **backend.transport.get_openapi_login_responses_success(),
    }

    @router.post(
        "/refresh",
        name=f"auth:{backend.name}.refresh",
        responses=refresh_responses,
    )
    async def refresh(
        user_manager: Annotated[
            BaseUserManager[models.UP, models.ID], Depends(get_user_manager)
        ],
        strategy: Annotated[
            Strategy[models.UP, models.ID], Depends(backend.get_strategy)
        ],
        refresh_strategy: Annotated[
            Strategy[models.UP, models.ID], Depends(backend.get_refresh_strategy)
        ],
        user_token: Annotated[Tuple[models.UP, str], Depends(get_current_user_token)],
        refresh_token: Annotated[str | None, Cookie()],
    ):
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorCode.REFRESH_TOKEN_MISSING,
            )

        user = await refresh_strategy.read_token(refresh_token, user_manager)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorCode.REFRESH_TOKEN_INVALID,
            )
        return await backend.refresh(
            strategy, refresh_strategy, user, user_token, refresh_token
        )

    return router


class CustomFastAPIUsers(FastAPIUsers, Generic[models.UP, models.ID]):
    def get_auth_router(
        self,
        backend: AuthenticationBackendRefresh[models.UP, models.ID],
        requires_verification: bool = False,
    ) -> APIRouter:
        """
        Return an auth router for a given authentication backend.

        :param backend: The authentication backend instance.
        :param requires_verification: Whether the authentication
        require the user to be verified or not. Defaults to False.
        """
        return get_auth_refresh_router(
            backend,
            self.get_user_manager,
            self.authenticator,
            requires_verification,
        )
