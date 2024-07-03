from typing import Any
from core.Handler import Handler
from core.User import User


name = "Settings"
icon = "settings"

def __request_handler(handler: Handler, user: User, command: str, data: dict[str, Any]) -> dict[str, Any]:
    return {}

request_handler = __request_handler