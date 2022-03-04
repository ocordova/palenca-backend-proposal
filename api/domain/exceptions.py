from typing import Any, Dict
from ..misc.config import environment


class BaseException(Exception):
    """
    Base exception envelope
    """

    code = "error"
    message = ""
    documentation_url = ""

    def __init__(self, code=None, message=None, documentation_url=None) -> None:
        super().__init__(code, message, documentation_url)
        _documentation_url = documentation_url
        if isinstance(_documentation_url, str) and _documentation_url:
            self.documentation_url = (
                f"{environment.DOCUMENTATION_URI}/{_documentation_url}"
            )
        else:
            self.documentation_url = ""

    def serialize(self) -> Dict[str, Any]:
        """Serializes into a dictionary the exception, useful for JSON responses"""
        data = {
            "code": self.code,
            "message": self.message,
        }

        if self.documentation_url:
            data["documentation_url"] = self.documentation_url

        return data


class BusinessException(BaseException):
    """
    Exception that represents a business exception, becuase some usecases decided
    to raise this exception.

    """

    code = "business_error"
    message = "Business error"

    def __init__(self, code=None, message=None, documentation_url=None) -> None:
        super.__init__(code, message, documentation_url)


class NotFoundException(BaseException):
    """
    Exception that represent that an entity does not exist or client isn't properly authenticated
    """

    code = "not_found_error"
    message = "Not found"

    def __init__(self, code=None, message=None, documentation_url=None) -> None:
        super().__init__(code, message, documentation_url)


class UnauthorizedException(BaseException):
    """
    Exception that represent no valid API key provided
    """

    code = "unauthorized_error"
    message = "Unauthorized"

    def __init__(self, code=None, message=None, documentation_url=None) -> None:
        super().__init__(code, message, documentation_url)


class UnableToCreateUser(BusinessException):
    code = "unable_to_create_user"
    message = "We couldn't create a user, please try again in a few seconds"

