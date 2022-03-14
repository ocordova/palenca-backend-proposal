from pydantic import BaseModel, EmailStr

from api.domain.enums import CountryCode, Source


class PedidosYaCreateUserBody(BaseModel):
    user_id: str
    country: CountryCode
    email: EmailStr
    password: str
    worker_id: str
    source: Source | None = None

    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "user_id": "cl0qdh4tk000007l6gl7h2vg1",
                "country": "mx",
                "email": "jane.doe@gmail.com",
                "password": "53cr3t",
                "worker_id": "372634",
                "source": "widget",
            }
        }
