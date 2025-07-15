from fastapi import Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi_users.authentication import BearerTransport, CookieTransport
from fastapi_users.openapi import OpenAPIResponseType


class BearerResponseRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class BearerTransportRefresh(BearerTransport):
    async def get_login_response(self, token: str, refresh_token: str) -> Response:
        bearer_response = BearerResponseRefresh(
            access_token=token, refresh_token=refresh_token, token_type="bearer"
        )
        response = JSONResponse(bearer_response.dict())
        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        return response

    @staticmethod
    def get_openapi_login_responses_success() -> OpenAPIResponseType:
        return {
            status.HTTP_200_OK: {
                "model": BearerResponseRefresh,
                "content": {
                    "application/json": {
                        "example": {
                            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1"
                            "c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2Z"
                            "DMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS"
                            "11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ."
                            "M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
                            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1"
                            "c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2Z"
                            "DMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS"
                            "11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ."
                            "M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
                            "token_type": "bearer",
                        }
                    }
                },
            },
        }


class CookieTransportRefresh(CookieTransport):
    def __init__(
        self,
        cookie_name="access_token",
        refresh_cookie_name="refresh_token",
        cookie_max_age=None,
        refresh_cookie_max_age=None,
        cookie_path="/",
        cookie_domain=None,
        cookie_secure=True,
        cookie_httponly=True,
        cookie_samesite="lax",
    ):
        super().__init__(
            cookie_name,
            cookie_max_age,
            cookie_path,
            cookie_domain,
            cookie_secure,
            cookie_httponly,
            cookie_samesite,
        )
        self.refresh_cookie_name = refresh_cookie_name
        self.refresh_cookie_max_age = refresh_cookie_max_age

    async def get_login_response(self, token: str, refresh_token: str) -> Response:
        response = Response(status_code=status.HTTP_204_NO_CONTENT)
        response = self._set_login_cookie(response, token, refresh_token)
        return response

    async def get_logout_response(self) -> Response:
        response = Response(status_code=status.HTTP_204_NO_CONTENT)
        return self._set_logout_cookie(response)

    def _set_login_cookie(
        self, response: Response, token: str, refresh_token: str
    ) -> Response:
        response.set_cookie(
            self.cookie_name,
            token,
            max_age=self.cookie_max_age,
            path=self.cookie_path,
            domain=self.cookie_domain,
            secure=self.cookie_secure,
            httponly=self.cookie_httponly,
            samesite=self.cookie_samesite,
        )
        response.set_cookie(
            self.refresh_cookie_name,
            refresh_token,
            max_age=self.refresh_cookie_max_age,
            path=self.cookie_path,
            domain=self.cookie_domain,
            secure=self.cookie_secure,
            httponly=self.cookie_httponly,
            samesite=self.cookie_samesite,
        )
        return response

    def _set_logout_cookie(self, response: Response) -> Response:
        response.set_cookie(
            self.cookie_name,
            "",
            max_age=0,
            path=self.cookie_path,
            domain=self.cookie_domain,
            secure=self.cookie_secure,
            httponly=self.cookie_httponly,
            samesite=self.cookie_samesite,
        )
        response.set_cookie(
            self.refresh_cookie_name,
            "",
            max_age=0,
            path=self.cookie_path,
            domain=self.cookie_domain,
            secure=self.cookie_secure,
            httponly=self.cookie_httponly,
            samesite=self.cookie_samesite,
        )
        return response
