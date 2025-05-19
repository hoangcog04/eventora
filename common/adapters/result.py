from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from common.enums.code import Code


@dataclass
class Result:
    code: int
    message: str
    data: Optional[Union[Dict, List]] = None


def success(code=Code.SUCCESS, data=None) -> "Result":
    return Result(code=code.code, message=code.message, data=data)


def failed(code=Code.FAILED) -> "Result":
    return Result(code=code.code, message=code.message, data=None)
