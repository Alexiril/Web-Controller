from typing import Any

# Configuration caching

__configuration: None | dict[str, Any] = None
__config_read = False

# Actual configuration values

APPS: dict[str, str] = {}
USERS: dict[str, Any] = {}
SERVER: dict[str, Any] = {}

def __read_config() -> None:
    """
    Internal function that loads the application.config
    JSON file and sets the configuration values.
    
    * Works only if the global __config_read flag is set to False to
    prevent updating configuration from file each request.
    """
    global __config_read
    if __config_read:
        return
    global __configuration
    from json import JSONDecoder
    from os.path import exists, isfile
    if not exists('application.config') or not isfile('application.config'):
        return
    with open('application.config') as file:
        __configuration = JSONDecoder().decode(file.read())
    __config_read = True
    config_map: dict[str, str] = {
        "APPS": "Applications",
        "USERS": "Users",
        "SERVER": "Server"
    }
    from sys import modules
    this = modules[__name__]
    for key, value in config_map.items():
        setattr(this, key, 
                getattr(__configuration, 'get', lambda _, y: y)
                (value, getattr(this, key, None)))

__read_config()