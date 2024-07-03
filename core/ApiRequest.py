from typing import Any, TYPE_CHECKING

from jwt import decode

from core.Config import CSRF_TOKEN_LENGTH, read_config
from core.Exceptions import IncorrectApiRequestException, IncorrectCSRFTokenException, UnauthorizedException
from core.ReadFile import ReadFile

if TYPE_CHECKING:
    from core.User import User
    from core.Handler import Handler

class ApiRequest:

    
    def __init__(self,
                 handler: "Handler",
                 expected_command: str,
                 expected_args: set[str],
                 user: "User | None",
                 data: dict[str, Any],
                 needs_csrf: bool = False,
                 needs_user: bool = False,
                 check_command: bool = True) -> None:
        if handler.command != expected_command and check_command:
            raise IncorrectApiRequestException(f"API request was not {expected_command}.")
        self.handler: "Handler" = handler
        self.user: "User | None" = user
        if needs_user and self.user == None:
            raise UnauthorizedException("API request requires authentication.")
        self._expected_args: set[str] = expected_args
        self.data: dict[str, Any] = data
        self.check_args()
        if needs_csrf and not self.check_csrf():
            raise IncorrectCSRFTokenException(
                f"Incorrect CSRF protection token."
            )

    def check_csrf(self) -> bool:
        if 'csrf' not in self.data:
            raise IncorrectApiRequestException(
                f"No 'csrf' argument in request data"
            )
        server_conf = read_config("Server", dict[str, Any])
        try:
            audience = server_conf.get('issuer-claim', 'example:issuer') + \
                "@" + server_conf.get('bind-domain', 'web')
            data: dict[str, Any] = decode(
                self.data['csrf'],
                ReadFile(server_conf.get("auth-public-key", "")).decode(),
                ["RS512"],
                verify=True,
                audience=audience,
                issuer=server_conf.get("issuer-claim", "example:issuer")
            )
            if data["dest"] != "csrfprotection" or len(data["random"]) != CSRF_TOKEN_LENGTH:
                return False
            return True
        except:
            return False

    def check_args(self) -> None:
        for arg in self._expected_args:
            if arg not in self.data:
                raise IncorrectApiRequestException(
                    f"No '{arg}' argument in request data"
                )

    def __call__(self) -> dict[str, Any] | list[Any] | str | int | float | bool:
        return ""