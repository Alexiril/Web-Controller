from os import path

from core.Exceptions import NoFileException

def ReadFile(url: str) -> bytes:
    if (path.exists(url) and path.isfile(url)):
        with open(url,"br") as op:
            return op.read()
    raise NoFileException(url)