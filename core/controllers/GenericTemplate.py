from typing import Any
from core.Config import read_config
from core.Template import Template
from core.controllers.Redirect import RedirectController
from core.Controller import Controller
from core.Application import applications


class GenericTemplateController(Controller):

    def __init__(self,
                 template_file: str,
                 variables: dict[str, Any],
                 needs_user: bool = False) -> None:
        self.template_file = template_file
        self.needs_user = needs_user
        server_conf = read_config("Server", dict[str, Any])
        self.variables = {
            "SITE_NAME": server_conf.get("site-name", "Web controller"),
            "SITE_PROTO": 'https' if server_conf.get("use-ssl", False) else 'http',
            "SITE_IP": server_conf.get("bind-domain", "localhost")
        }
        self.variables.update(variables)

    def __call__(self, handler, arguments, user) -> bytes:
        if user is None and self.needs_user:
            return RedirectController('/auth')(handler, arguments, user)
        apps = [] if user is None else user.granted_apps
        with applications as _apps:
            apps = [
                (_apps[x].id, _apps[x].name, _apps[x].icon) for x in apps if x in _apps]
        self.variables.update({
            'ARGUMENTS': str(arguments),
            'URL': str(handler.path),
            'USER_IN': user is not None,
            'USER_BACKGROUND': '' if user is None else user.background,
            'USER_NAME': '' if user is None else user.name,
            'USER_ID': '' if user is None else user.id,
            'USER_PFP': '' if user is None else user.profile_picture,
            'APPLICATIONS': apps 
        })
        return Template(self.template_file, self.variables, user).result.encode()