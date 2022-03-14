from api.misc.config import environment


class BaseHTTPException(Exception):
    """
    Base http exception envelope
    """

    code = 500

    def __init__(
        self,
        code=None,
    ) -> None:
        super().__init__(code)


class BusinessHTTPException(BaseHTTPException):
    """
    HTTP 400 Error
    """

    code = 400


class UnauthorizedHTTPException(BaseHTTPException):
    """
    HTTP 401 Error
    """

    code = 401


class ForbiddenHTTPException(BaseHTTPException):
    """
    HTTP 403 Error
    """

    code = 403


class NotFoundHTTPException(BaseHTTPException):
    """
    HTTP 404 Error
    """

    code = 404


class TooManyRequestsHTTPException(BaseHTTPException):
    """
    HTTP 429 Error
    """

    code = 429


class InternalServerHTTPException(BaseHTTPException):
    """
    HTTP 500 Error
    """

    code = 500
