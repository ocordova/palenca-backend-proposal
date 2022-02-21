from functools import wraps
from importlib import util as importlib_util
from re import split
from typing import Dict, Optional, Tuple

from flask import abort, json, make_response
from ..misc.exceptions import BusinessException

marshmallow_spec = importlib_util.find_spec("marshmallow")
mongoengine_spec = importlib_util.find_spec("mongoengine")


def build_validation_error_response(*, errors: Dict) -> Tuple[Dict, int]:
    """Function that builds the error response that the frontend expects
    when a validation error ocurrs while parsing the request arguments

    :param Dict errors: The errors thaat were thrown by marshmallow (or any other library),
        when doing a validation.
    :return: Tuple[str, int]
        - Dict[str, Dict] [0] - The errors passed as an argument, inside a dictionary with
            the key errors
        - int [1] - The number 422, which tells us the error we should return on flask is an HTTP 422 code.

    ============================
             Example
    ============================

    In[1]: errors = {"name": ["Name is not valid"]}
    In[2]: build_validation_error_response(errors=errors)
    Out[2]: ({"errors": {"name": ["Name is not valid"]}}, 422)
    """
    return {"errors": errors}, 422


def build_business_error_response(*, errors: Dict) -> Tuple[Dict, int]:
    """Function that builds the error response that the frontend expects
    when a business error ocurrs.

    :param Dict errors: The errors that were thrown by the business exception.
    :return: Tuple[str, int]
        - Dict[str, str] [0] - The errors passed as they are
        - int [1] - The number 409, which tells us the error we should return on flask is an HTTP 409 code.

    ============================
             Example
    ============================

    In[1]: errors = {"code": "code", "message": "message·}
    In[2]: build_business_error_response(errors=errors)
    Out[2]: ({"code": "code", "message": "message·}, 409)
    """
    return errors, 409


def parse_errors(func):
    """A decorator that wraps a flask view, and parses the exceptions that could happen
    returning or raising a correspondent value, depending on the exception.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if marshmallow_spec:
                from marshmallow import exceptions

                if isinstance(e, exceptions.ValidationError):
                    return build_validation_error_response(errors=e.messages)

            if mongoengine_spec:
                from bson.errors import InvalidId
                from mongoengine import DoesNotExist

                if isinstance(e, DoesNotExist):
                    abort(404)
                elif isinstance(e, InvalidId):
                    abort(400)

            if isinstance(e, BusinessException):
                return build_business_error_response(errors=e.serialize())

            raise e

    return wrapper


def handle_exception(e: Exception):
    """Return JSON instead of HTML for HTTP errors."""
    try:
        raise e
    except:
        import traceback

        traceback.print_exc()
    data = json.dumps({"code": "server_error", "message": repr(type(e).__name__),})
    response = make_response(data, 500)
    response.content_type = "application/json"
    return response
