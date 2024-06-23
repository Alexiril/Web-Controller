from re import match
from typing import TYPE_CHECKING
from core.Config import SERVER
from core.Exceptions import NotFoundException
from core.controllers.Api import ApiController
from core.controllers.Application import ApplicationController
from core.controllers.Assets import AssetsController
from core.controllers.GenericTemplate import GenericTemplateController
from core.controllers.Redirect import RedirectController
from core.interfaces.Controller import Controller
from core.interfaces.Route import Route

if TYPE_CHECKING:
    from core.Handler import Handler

class Router:

    def __init__(self) -> None:
        self.clear()

    def add_route(self, regex: str, controller: Controller):
        self._routes.append(Route(regex, controller))

    def route(self, handler: "Handler", url: str):
        for r in self._routes:
            if (m := match(r.regex, url)) != None:
                return r.controller(handler, m.groups())
        raise NotFoundException(url)
    
    def clear(self):
        self._routes: list[Route] = []

_routes_cached: bool = False
_router: Router = Router()

def _setup_routes() -> Router | None:
    global _routes_cached
    if _routes_cached and SERVER.get("cache-router", True):
        return
    if SERVER.get("routes-debug", False):
        print("\033[94mBuilding routes...\033[0m")
    router = Router()
    router.add_route(r"^/favicon\.ico$", RedirectController("$assets/favicon.ico"))
    router.add_route(r"^/\$assets/(.*)$", AssetsController())
    router.add_route(r"^/auth$", GenericTemplateController('templates/auth.html', {}))
    router.add_route(r"^/api/(.+)$", ApiController())
    router.add_route(r"^/$", ApplicationController())
    _routes_cached = True
    return router

def get_router() -> Router:
    global _router
    if (r := _setup_routes()) != None:
        _router = r
    return _router