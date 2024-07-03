from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.User import User
    from core.Handler import Handler

class Controller:

    
    def __init__(self) -> None:
        pass

    def __call__(self,
                 handler: "Handler",
                 arguments: tuple[str | Any, ...],
                 user: "User | None") -> bytes:
        return b""