from pydantic import BaseModel

from api.domain.exceptions import InvalidCredentialsException


class BaseErrorResponse(BaseModel):
    code: str
    message: str
    documentation_url: str


class HealthResponse(BaseModel):
    status: int


class SucessfullLoginResponse(BaseModel):
    user_id: str

    class Config:
        schema_extra = {"example": {"user_id": "cl0qcob2u000009lc2i4t3l14"}}


class CreateUserExceptionResponse(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "code": InvalidCredentialsException.code,
                "message": InvalidCredentialsException.message,
            }
        }
