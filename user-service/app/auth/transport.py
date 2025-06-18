from fastapi import Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi_users.authentication import BearerTransport
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
        return JSONResponse(bearer_response.dict())

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
