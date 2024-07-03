import hashlib
from http.cookies import SimpleCookie
from threading import Lock
from typing import TYPE_CHECKING, Any
from jwt import InvalidTokenError, decode

from core.Config import read_config
from core.LockObject import LockObject
from core.ReadFile import ReadFile

if TYPE_CHECKING:
    from core.Handler import Handler

class User:

    
    def __init__(self, id: str, name: str, key: str,
                 granted_apps: list[str], app_cookies: dict[str, dict[str, str]],
                 background: str, profile_picture: str) -> None:
        self.id: str = id
        self.name: str = name
        self.key: str = key
        self.granted_apps: list[str] = granted_apps
        self.app_cookies: dict[str, dict[str, str]] = app_cookies
        self.background: str = background
        self.profile_picture: str = profile_picture

    def check_key(self, password: str) -> bool:
        key = hashlib.new("sha3_512", password.encode()).hexdigest()
        return key == self.key

users: LockObject[dict[str, User]] = LockObject(dict[str, User])
_users_added_lock = Lock()
with _users_added_lock:
    _users_added = False
def initialize() -> None:
    global _users_added
    with _users_added_lock:
        if _users_added: return
    for id, value in read_config("Users", dict[str, Any]).items():
        with users as _users:
            _users[id] = User(id,
                     value.get("name", id),
                     value.get("key", ""),
                     value.get("granted-apps", []),
                     value.get("app-cookies", {}),
                     value.get("background", ""),
                     value.get("profile-picture", ""))
    with _users_added_lock:
        _users_added = True

def auth_user(handler: "Handler") -> User | None:
    cookies = SimpleCookie(handler.headers.get('Cookie', ''))
    if (token := cookies.get('token')) == None:
        return
    server_conf = read_config("Server", dict[str, Any])
    try:
        data: dict[str, Any] = decode(
            token.value,
            ReadFile(server_conf.get("auth-public-key", "")).decode(),
            ["RS512"],
            verify=True,
            audience=f"{server_conf.get(
                'issuer-claim', 'example:issuer')}@{server_conf.get('bind-domain', 'web')}",
            issuer=server_conf.get("issuer-claim", "example:issuer")
        )
        with users as _users:
            if (id := data.get('id')) == None or \
                id not in _users or \
                _users[id].key != data.get('key', ''):
                return
            return _users[id]
    except InvalidTokenError:
        return