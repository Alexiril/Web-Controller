from core.interfaces.Controller import Controller


class ApiController(Controller):

    def __init__(self) -> None:
        pass

    def __call__(self, handler, arguments) -> bytes:
        return b""