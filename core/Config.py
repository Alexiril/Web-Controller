from datetime import timedelta
from threading import Lock
from typing import Any

from core.Exceptions import ConfigException
from core.LockObject import LockObject

# Configuration caching

_configuration: LockObject[dict[str, Any]] = LockObject(dict[str, Any])
_config_read = False
_config_read_lock = Lock()

# Actual configuration values

CSRF_TOKEN_LENGTH: int = 128
CSRF_TOKEN_LIVES: timedelta = timedelta(minutes=10)
AUTH_TOKEN_LIVES: timedelta = timedelta(days=1)


def read_config[T](config_value: str, result_type: type[T] = type(Any)) -> T:
    global _config_read, _configuration, _config_read_lock
    with _config_read_lock:
        if not _config_read:
            from json import JSONDecoder
            from os.path import exists, isfile
            if not exists('application.config') or not isfile('application.config'):
                raise ConfigException("Configuration file doesn't exist.")
            with open('application.config') as file:
                _configuration.reset(JSONDecoder().decode(file.read()))
            _config_read = True
    with _configuration as conf:
            return conf[config_value]