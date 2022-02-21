from pydantic import BaseModel


class BaseEmptySuccessResponse(BaseModel):
    code: str
    message: str


class OTPSentSuccessfullyResponse(BaseEmptySuccessResponse):
    code: str = "otp_sent_successfully"
    message: str = "The OTP was sent to the device successfully"
