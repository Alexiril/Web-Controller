from http import HTTPStatus
from core.Controller import Controller

class RedirectController(Controller):

    def __init__(self, redirect_to: str) -> None:
        self.redirect_to = redirect_to

    def __call__(self, handler, arguments, user) -> bytes:
        handler.reactive_response = HTTPStatus.FOUND.value
        handler.reactive_headers['Location'] = self.redirect_to
        return b""