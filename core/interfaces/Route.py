from core.interfaces.Controller import Controller

class Route:

    def __init__(self, regex: str, controller: Controller) -> None:
        self.regex: str = regex
        self.controller: Controller = controller
