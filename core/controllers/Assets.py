from os.path import join, exists, isfile, realpath
from pathlib import PurePath
from urllib.parse import unquote
from core.Exceptions import BadRequestException, NotFoundException
from core.Functions import read_file
from core.interfaces.Controller import Controller
from core.Mime import known_types

class AssetsController(Controller):

    def __call__(self, handler, arguments) -> bytes:
        if len(arguments) != 1:
            raise BadRequestException("Cannot handle $assets request.")
        real_path = realpath(join("assets", unquote(arguments[0])))
        try:
            PurePath(real_path).relative_to(PurePath(realpath("./assets")))
        except ValueError:
            raise NotFoundException(unquote(arguments[0]))
        if not exists(real_path) or not isfile(real_path):
            raise NotFoundException(unquote(arguments[0]))
        else:
            handler.reactive_headers["Content-Type"] = known_types.get(real_path.split(".")[-1], "application/octet-stream")
            return read_file(real_path)