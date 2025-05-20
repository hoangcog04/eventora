from dataclasses import dataclass
from typing import Any, Dict, Optional

from common.constants.code import Status


@dataclass
class Result:
    code: int
    message: str
    data: Optional[Any] = None


def success(data=None, status=Status.SUCCESS) -> Dict[str, Any]:
    return Result(status.code, status.msg, data).__dict__


def failed(data=None, status=Status.FAILED) -> Dict[str, Any]:
    return Result(status.code, status.msg, data).__dict__


def validate_failed(data=None, status=Status.VALIDATE_FAILED) -> Dict[str, Any]:
    return Result(status.code, status.msg, data).__dict__
