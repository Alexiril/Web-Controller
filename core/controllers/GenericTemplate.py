from core.Config import SERVER
from core.Functions import read_file, template
from core.interfaces.Controller import Controller


class GenericTemplateController(Controller):

    def __init__(self, template_file, variables) -> None:
        self.template_file = template_file
        self.variables = {
            "SITE_NAME": SERVER.get("site-name", "Web controller"),
            "USER_BACKGROUND": ""
        }
        self.variables.update(variables)

    def __call__(self, handler, arguments) -> bytes:
        self.variables['ARGUMENTS'] = str(arguments)
        return template(read_file(self.template_file).decode(), self.variables).encode()