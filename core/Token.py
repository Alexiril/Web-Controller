from datetime import datetime, timedelta, timezone
from random import SystemRandom
from string import ascii_lowercase, ascii_uppercase, digits
from typing import Any
from jwt import encode
from core.Config import AUTH_TOKEN_LIVES, CSRF_TOKEN_LENGTH, CSRF_TOKEN_LIVES, read_config
from core.Exceptions import NoAuthKeyException
from core.User import User
from core.ReadFile import ReadFile

def MakeGenericToken(payload: dict[str, Any], delta: timedelta) -> str:
    server_conf = read_config("Server", dict[str, Any])
    if "auth-private-key" not in server_conf:
        raise NoAuthKeyException("Private authentication key is not set in the server.")
    payload.update({
        "iss": server_conf.get("issuer-claim", "example:issuer"),
        "exp": datetime.now(tz=timezone.utc) + delta,
        "iat": datetime.now(tz=timezone.utc),
        "aud": f"{server_conf.get('issuer-claim', 'example:issuer')}@{server_conf.get('bind-domain', 'web')}"
    })
    return encode(payload, ReadFile(server_conf.get("auth-private-key", "")).decode(), "RS512")

def MakeAuthToken(user: User) -> str:
    return MakeGenericToken({
        "dest": "auth",
        "id": user.id,
        "key": user.key
    }, AUTH_TOKEN_LIVES)
    
def MakeCSRFProtectionToken() -> str:
    return MakeGenericToken({
        "dest": "csrfprotection",
        "random": ''.join(SystemRandom()
                         .choice(ascii_lowercase + ascii_uppercase + digits) for _ in range(CSRF_TOKEN_LENGTH))
    }, CSRF_TOKEN_LIVES)