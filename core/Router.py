from re import match
from threading import Lock
from typing import TYPE_CHECKING, Any
from core.Config import read_config
from core.Exceptions import NotFoundException
from core.controllers.Api import ApiController
from core.controllers.Assets import AssetsController
from core.controllers.GenericTemplate import GenericTemplateController
from core.controllers.Redirect import RedirectController
from core.LockObject import LockObject
from core.Controller import Controller

if TYPE_CHECKING:
    from core.Handler import Handler
    from core.User import User

class Route:

    
    def __init__(self, regex: str, controller: Controller) -> None:
        self.regex: str = regex
        self.controller: Controller = controller

class Router:

    
    def __init__(self, routes: list[Route]) -> None:
        self._routes = routes.copy()

    def route(self, handler: "Handler", url: str, user: "User | None") -> bytes:
        for r in self._routes:
            if (m := match(r.regex, url)) != None:
                return r.controller(handler, m.groups(), user)
        raise NotFoundException(url)


_router_cached_lock = Lock()
with _router_cached_lock:
    _routes_cached: bool = False
router: LockObject[Router] = LockObject(Router, [])


def initialize() -> None:
    global _routes_cached, router
    with _router_cached_lock:
        server_conf = read_config("Server", dict[str, Any])
        if _routes_cached and server_conf.get("cache-router", True):
            return
        if server_conf.get("routes-debug", False):
            print("\033[94mBuilding routes...\033[0m")
    router.reset(Router([
        Route(r"^/favicon\.ico$",
              RedirectController('$assets/favicon.ico')),
        Route(r"^/\$assets/(.*)$",
              AssetsController()),
        Route(r"^/auth$",
              GenericTemplateController('templates/auth.html', {})),
        Route(r"^/\$api/(.+)$",
              ApiController()),
        Route(r"^/$",
              GenericTemplateController('templates/empty.app.html', {}, True))
    ]))
    with _router_cached_lock:
        _routes_cached = True