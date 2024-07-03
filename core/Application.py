from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from os.path import exists, isdir, join
from threading import Lock
from typing import Callable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from core.User import User
    from core.Handler import Handler

from core.Config import read_config
from core.Exceptions import ApplicationLoadingException
from core.LockObject import LockObject

class Application:

    
    def __init__(self,
                 id: str,
                 path: str,
                 request_handler: Callable[["Handler", "User", str, dict[str, Any]], Any],
                 name: str,
                 icon: str) -> None:
        self.id: str = id
        self.path: str = path
        self.request_handler = request_handler
        self.name: str = name
        self.icon: str = icon

def _load_app(id, path) -> Application:
    if not exists(path):
        ApplicationLoadingException(f"Application {id} at {path} doesn't exist.")
    if not isdir(path):
        ApplicationLoadingException(f"Application {id} at {path} is not a folder.")
    path = join(path, "app.py")
    if not exists(path):
        ApplicationLoadingException(
            f"Application {id} at {path} doesn't exist (app.py file).")

    loader = SourceFileLoader('__appconfigurationfile', path)
    spec = spec_from_loader(loader.name, loader)
    if spec == None:
        raise ApplicationLoadingException(f"Cannot load application {id} at {path}.")
    module = module_from_spec(spec)
    loader.exec_module(module)
    if (handler := getattr(module, "request_handler", None)) == None:
        raise ApplicationLoadingException(
            f"Application {id} at {path} doesn't have application router.")
    icon: str = getattr(module, "icon", "")
    name: str = getattr(module, "name", id)
    return Application(id, path, handler, name, icon)
        
applications: LockObject[dict[str, Application]] = LockObject(dict[str, Application])
_apps_added_lock = Lock()
with _apps_added_lock:
    _apps_added = False
def initialize() -> None:
    global _apps_added
    with _apps_added_lock:
        if _apps_added: return
    with applications as _apps:
        conf = read_config('Applications', dict[str, str])
        for id, value in conf.items():
            _apps[id] = _load_app(id, value)
    with _apps_added_lock:
        _apps_added = True