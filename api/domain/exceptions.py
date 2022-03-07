from email import message
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
    Serialized as HTTP 400 Error
    """

    code = "business_error"
    message = "Business error"

    def __init__(self, code=None, message=None, documentation_url=None) -> None:
        super.__init__(code, message, documentation_url)


class UnauthorizedException(BaseException):
    """
    Exception that represent the lack of valid authentication credentials
    Serialized as HTTP 401 Error
    """

    code = "unauthorized_error"
    message = "Unauthorized"

    def __init__(self, code=None, message=None, documentation_url=None) -> None:
        super().__init__(code, message, documentation_url)


class ForbiddenException(BaseException):
    """
    Exception that represent server understands the request but refuses to authorize it
    Serialized as HTTP 403 Error
    """

    code = "forbidden_error"
    message = "The API key doesn't have permissions to perform the request"


class NotFoundException(BaseException):
    """
    Exception that represent that an entity does not exist or client isn't properly authenticated
    Serialized as HTTP 404 Error
    """

    code = "not_found_error"
    message = "Not found"

    def __init__(self, code=None, message=None, documentation_url=None) -> None:
        super().__init__(code, message, documentation_url)


class TooManyRequestsException(BaseException):
    """
    Exception that represent the server encountered an unexpected condition
    Serialized as HTTP 429 Error
    """

    code = "too_many_requests_error"
    message = "Too many requests hit the API too quickly."

    def __init__(self, code=None, message=None, documentation_url=None) -> None:
        super().__init__(code, message, documentation_url)


class InternalServerException(BaseException):
    """
    Exception that represent the server encountered an unexpected condition
    Serialized as HTTP 500 Error
    """

    code = "internal_server_error"
    message = "The server encountered an unexpected condition"

    def __init__(self, code=None, message=None, documentation_url=None) -> None:
        super().__init__(code, message, documentation_url)


"""
Business Expcetions
"""


class UnableToCreateUserException(BusinessException):
    code = "unable_to_create_user_error"
    message = "We couldn't create a user, please try again in a few seconds"


class PlatformUnavailableInCountryException(BusinessException):
    code = "platform_unavailable_in_country_error"
    message = "The platform is not available in the country"


class PlatformIsNotOperatingException(BusinessException):
    code = "platform_is_not_operating_error"
    message = "The platform is not operating"


class InvalidCredentialsException(BusinessException):
    code = "invalid_credentials_error"
    message = "The credentials are not valid"
    documentation_url = "#platforms__invalid_credentials"


class PlatformConnectivityException(BusinessException):
    code = "platform_connectivity_error"
    message = (
        "We were unable to connect with the platform, wait a few minutes and try again"
    )
    documentation = "#platforms__connectivity_exception"
