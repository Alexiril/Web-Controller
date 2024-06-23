from http import HTTPStatus
from core.controllers.Redirect import RedirectController
from core.interfaces.Controller import Controller


class ApplicationController(Controller):

    def __init__(self) -> None:
        pass

    def __call__(self, handler, arguments) -> bytes:
        if handler.headers["Authorization"] == None:
            return RedirectController("/auth")(handler, ())
        return b""