from enum import Enum


class Code(Enum):
    SUCCESS = (200, "Operation successful")
    VALIDATE_FAILED = (400, "Parameter verification failed")
    UNAUTHORIZED = (401, "Not logged in or token has expired")
    FORBIDDEN = (403, "You do not have permission to access the resource you requested")
    NOT_FOUND = (404, "Not found")
    FAILED = (500, "Operation failed")

    def __init__(self, code, message):
        self.code = code
        self.message = message
