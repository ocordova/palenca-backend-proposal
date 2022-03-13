from pydantic import BaseModel
from mock.pedidosya.domain.enums import ContractType


class Authentication(BaseModel):
    token: str
    contract_type: ContractType
    id_verification_required: bool
    city_id: int
    city_name: str
