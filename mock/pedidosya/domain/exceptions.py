from email import message
from typing import Any, Dict, Union


class BaseException(Exception):
    """
    Base exception envelope
    """

    status = 0
    message = ""

    def __init__(self, status=None, message=None) -> None:
        super().__init__(status, message)

    def serialize(self) -> Dict[str, Any]:
        """Serializes into a dictionary the exception, useful for JSON responses"""
        data: Dict[str, Any] = {
            "message": self.message,
        }

        if self.status:
            data["status"] = self.status

        return data


class UnauthorizedException(BaseException):
    """
    Exception that represent the lack of valid authentication credentials
    Serialized as HTTP 401 Error
    """

    status = 401
    message = "Error IAL401: Invalid credentials"
