from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.Handler import Handler


class Controller:

    def __init__(self) -> None:
        pass

    def __call__(self, handler: "Handler", arguments: tuple[str | Any, ...]) -> bytes:
        return b""