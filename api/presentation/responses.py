from pydantic import BaseModel


class BaseEmptySuccessResponse(BaseModel):
    code: str
    message: str


class OTPSentSuccessfullyResponse(BaseEmptySuccessResponse):
    code = "otp_sent_successfully"
    message = "The OTP was sent to the device successfully"


class HealthResponse(BaseModel):
    status: int


class SucessfullLogin(BaseEmptySuccessResponse):
    code = "successfull_login"
    message = "The login to the platform was successcull"
    user_id: str
