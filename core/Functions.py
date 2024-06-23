from os import path
from re import search
from typing import Any

from core.Exceptions import NoFileException, TemplateException

def read_file(url: str) -> bytes:
    if (path.exists(url) and path.isfile(url)):
        with open(url,"br") as op:
            return op.read()
    raise NoFileException(url)
    
def template(text: str, variables: dict[str, Any]) -> str:
    while (m := search(r"{{([^}]*)}}", text)) != None:
        var = m.group(1).strip()
        if (m_inc := search(r"^ *include *: *(.+) *$", var)) != None:
            result = template(read_file(m_inc.group(1)).decode(), variables)
        elif var not in variables:
            raise TemplateException(f"Incorrect variable '{var}' in template.")
        else:
            result = str(variables[var])
        text = text.replace(m.group(0), result)
    return text