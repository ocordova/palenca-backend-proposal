from typing import Any, Dict


class BusinessException(Exception):
    """
    Exception that represents a business exception, becuase some usecases decided
    to raise this exception.

    """

    ERROR_CODE = "business_error"
    ERROR_MESSAGE = "Business error"
    extra_info: Dict[Any, Any]
    extra_info = {}

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        _extra_info = kwargs.get("extra_info", {})
        if isinstance(_extra_info, dict) and _extra_info:
            self.extra_info = _extra_info
        else:
            self.extra_info = {}

    def serialize(self) -> Dict[str, Any]:
        """Serializes into a dictionary the exception, useful for JSON responses"""
        return {
            "code": self.ERROR_CODE,
            "message": self.ERROR_MESSAGE,
            "extra_info": self.extra_info,
        }
