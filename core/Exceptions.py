from http import HTTPStatus
from typing import Any

def log_exception(exception) -> None:
    from core.Config import read_config
    server = read_config('Server', dict[str, Any])
    if server.get("print-errors", True):
        if server.get("print-http-errors", False) or \
            BaseHTTPException not in type(exception).mro():
            print("\033[91mError:", repr(exception), "\033[0m")

class ExtendedException(Exception):

    
    def __init__(self,
                 ecode: int = 0x1,
                 response: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
                 *args: object) -> None:
        self.ecode: int = ecode
        self.response: HTTPStatus = response
        super().__init__(*args)

class ConfigException(ExtendedException):

    def __init__(self, *args: object) -> None:
        super().__init__(ecode=0x10, *args)

class LockObjectException(ExtendedException):

    def __init__(self,
                 exception_type,
                 exception_value,
                 exception_traceback, *args: object) -> None:
        self.etype = exception_type
        self.evalue = exception_value
        self.etraceback = exception_traceback
        super().__init__(0x11, HTTPStatus.INTERNAL_SERVER_ERROR, *args)

    def __str__(self) -> str:
        return f"{self.etype.__name__} - {self.evalue} {self.args}"
    
    def __repr__(self) -> str:
        return str(self)
    
class BaseHTTPException(ExtendedException):

    
    def __init__(self,
                 response: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
                 *args: object) -> None:
        super().__init__(0x12, response, *args)

class BadRequestException(BaseHTTPException):
    
    def __init__(self, *args: object) -> None:
        super().__init__(HTTPStatus.BAD_REQUEST, *args)

class UnauthorizedException(BaseHTTPException):
    
    def __init__(self, *args: object) -> None:
        super().__init__(HTTPStatus.UNAUTHORIZED, *args)

class ForbiddenException(BaseHTTPException):

    def __init__(self, *args: object) -> None:
        super().__init__(HTTPStatus.FORBIDDEN, *args)

class NotFoundException(BaseHTTPException):
    
    def __init__(self, *args: object) -> None:
        super().__init__(HTTPStatus.NOT_FOUND, *args)

class RequestTimeoutException(BaseHTTPException):

    def __init__(self, *args: object) -> None:
        super().__init__(HTTPStatus.REQUEST_TIMEOUT, *args)

class TooManyRequestsException(BaseHTTPException):
    
    def __init__(self, *args: object) -> None:
        super().__init__(HTTPStatus.TOO_MANY_REQUESTS, *args)

class InternalException(BaseHTTPException):

    def __init__(self, *args: object) -> None:
        super().__init__(HTTPStatus.INTERNAL_SERVER_ERROR, *args)

class ServiceUnavailableException(BaseHTTPException):

    def __init__(self, *args: object) -> None:
        super().__init__(HTTPStatus.SERVICE_UNAVAILABLE, *args)

class TemplateException(ExtendedException):

    def __init__(self, *args: object) -> None:
        self.where: str = ""
        super().__init__(0x13, HTTPStatus.INTERNAL_SERVER_ERROR, *args)

    def __str__(self) -> str:
        return super().__str__() + f" at {self.where}"

class NoFileException(ExtendedException):

    def __init__(self, *args: object) -> None:
        super().__init__(0x14, HTTPStatus.NOT_FOUND, *args)

class NoAuthKeyException(ExtendedException):

    def __init__(self, *args: object) -> None:
        super().__init__(0x15, HTTPStatus.INTERNAL_SERVER_ERROR, *args)

class IncorrectApiRequestException(ExtendedException):

    def __init__(self, *args: object) -> None:
        super().__init__(0x16, HTTPStatus.BAD_REQUEST, *args)

class IncorrectAuthAttemptException(ExtendedException):

    def __init__(self, *args: object) -> None:
        super().__init__(0x17, HTTPStatus.UNAUTHORIZED, *args)

class IncorrectCSRFTokenException(ExtendedException):

    def __init__(self, *args: object) -> None:
        super().__init__(0x18, HTTPStatus.UNAUTHORIZED, *args)

class ApplicationLoadingException(ExtendedException):

    def __init__(self, *args: object) -> None:
        super().__init__(0x19, HTTPStatus.INTERNAL_SERVER_ERROR, *args)

class IncorrectApplicationRequestException(ExtendedException):

    def __init__(self, *args: object) -> None:
        super().__init__(0x20, HTTPStatus.BAD_REQUEST, *args)