from http import HTTPStatus
from core.Functions import read_file, template
from core.Exceptions import *
from core.Config import SERVER
from core.interfaces.Controller import Controller

class ErrorController(Controller):

    def __init__(self, exception) -> None:
        self.exception = exception

    def __call__(self, handler, arguments) -> bytes:
        if type(self.exception) == BadRequestException: error_code = HTTPStatus.BAD_REQUEST
        elif type(self.exception) == UnauthorizedException: error_code = HTTPStatus.UNAUTHORIZED
        elif type(self.exception) == ForbiddenException: error_code = HTTPStatus.FORBIDDEN
        elif type(self.exception) == NotFoundException: error_code = HTTPStatus.NOT_FOUND
        elif type(self.exception) == RequestTimeoutException: error_code = HTTPStatus.REQUEST_TIMEOUT
        elif type(self.exception) == TooManyRequestsException: error_code = HTTPStatus.TOO_MANY_REQUESTS
        elif type(self.exception) == InternalException: error_code = HTTPStatus.INTERNAL_SERVER_ERROR
        elif type(self.exception) == ServiceUnavailableException: error_code = HTTPStatus.SERVICE_UNAVAILABLE
        else: error_code = HTTPStatus.INTERNAL_SERVER_ERROR
        handler.reactive_response = error_code.value
        human_name = error_code.phrase
        description = error_code.description
        additional_info = "Error data: " + str(self.exception)
        return template(read_file("templates/error.html").decode(), {
            "SITE_NAME": SERVER.get("site-name", "Web controller"),
            "USER_BACKGROUND": "",
            "ERROR_CODE": error_code.value,
            "ERROR_HUMAN_NAME": human_name,
            "ERROR_DESCRIPTION": description,
            "ADDITIONAL_ERROR_INFO": additional_info
        }).encode()
