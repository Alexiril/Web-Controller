from re import search, Match
from typing import Any, TYPE_CHECKING, Iterable

from core.Exceptions import TemplateException
from core.Token import MakeCSRFProtectionToken
from core.ReadFile import ReadFile

if TYPE_CHECKING:
    from core.User import User

class Template:

    class IFExpression:

        def __init__(self, start: int, param: str, var: str) -> None:
            self.start: int = start
            self.param: str = param
            self.var: str = var
            self.else_at: int = -1

    class FORExpression:

        def __init__(self, start: int, loop_variables: list[str], iterable: Iterable) -> None:
            self.start: int = start
            self.loop_variables: list[str] = loop_variables
            self.iterable: Iterable = iterable

    def __init__(self,
                 filename: str,
                 variables: dict[str, Any],
                 user: "User | None" = None,
                 local_variables: list[dict[str, Any]] = []) -> None:
        self.variables: dict[str, Any] = variables
        text = ReadFile(filename).decode()
        self.original_text: str = text
        self.statement_stack: list[Template.IFExpression | Template.FORExpression] = []
        self.local_variables: list[dict[str, Any]] = local_variables
        self.result: str = text
        self.user: "User | None" = user
        while (match := search(r"{{([^}]*)}}", self.result)) != None:
            try:
                self._handle_expr(match)
            except TemplateException as e:
                e.where = f"File '{filename}', line {text.count('\n', 0, match.start()) + 1}"
                raise e

    def _handle_expr(self, match: Match[str] | None) -> None:
        if type(match) != Match:
            return
        expr = match.group(1).strip()
        if (include_match := search(r"^ *include *: *(.+) *$", expr)) != None:
            self._handle_include(match, include_match.group(1))
        elif (if_match := search(r"^ *if *(.*) *: * *(.+) *$", expr)) != None:
            self._handle_if(match, if_match.group(1), if_match.group(2))
        elif search(r"^ *else *$", expr) != None:
            self._handle_else(match)
        elif search(r"^ *end *$", expr) != None:
            self._handle_end(match)
        elif search(r"^ *csrfprotection *$", expr.lower()) != None:
            self._handle_csrf(match)
        # TODO: finish template for-each loop
        # --- for each is not implemented yet!
        elif (for_match := search(r"^ *for *each *\(([^)]*)\) *in +(.+) *$", expr)) != None:
            self._handle_foreach(match, for_match.group(1), for_match.group(2))
        else:
            self._handle_variable(match, expr)

    def _handle_generic_variable(self, var: str) -> Any:
        if var not in self.variables:
            raise TemplateException(f"Incorrect expression '{var}' in template.")
        return self.variables[var]

    def _handle_include(self, match: Match[str], include_url: str) -> None:
        self.result = self.result.replace(
            match.group(0), 
            Template(
                include_url, 
                self.variables,
                self.user,
                self.local_variables
            ).result
        )
        
    def _handle_variable(self, match: Match[str], var: str) -> None:
        self.result = self.result.replace(
            match.group(0),
            str(self._handle_generic_variable(var))
        )

    def _handle_cond_param(self, param: str, var: str) -> bool:
        match param:
            case '':
                return bool(self._handle_generic_variable(var))
            case 'not':
                return not bool(self._handle_generic_variable(var))
            case _:
                raise TemplateException(f"Incorrect conditional parameter '{param}' in template.")

    def _handle_if(self, match: Match[str], param: str, var: str) -> None:
        self.statement_stack.append(Template.IFExpression(match.start(0), param, var))
        self.result = self.result.replace(
            match.group(0),
            "",
            1
        )

    def _handle_else(self, match: Match[str]) -> None:
        found = False
        for index in range(-1, -len(self.statement_stack) - 1, -1):
            value = self.statement_stack[index]
            if type(value) != Template.IFExpression:
                raise TemplateException("'else' statement doesn't have 'if' statement before")
            elif type(value) == Template.IFExpression:
                if value.else_at == -1:
                    found = True
                    value.else_at = match.start()
                    break
        if not found:
            raise TemplateException("'else' statement doesn't have 'if' statement before.")
        self.result = self.result.replace(
            match.group(0),
            "",
            1
        )

    def _handle_end(self, endif_match: Match[str]) -> None:
        expr = self.statement_stack.pop()
        if type(expr) == Template.IFExpression:
            if self._handle_cond_param(expr.param, expr.var):
                if expr.else_at == -1:
                    change_to = self.result[expr.start:endif_match.start()]
                else:
                    change_to = self.result[expr.start:expr.else_at]
            else:
                if expr.else_at == -1:
                    change_to = ""
                else:
                    change_to = self.result[expr.else_at:endif_match.start()]
            self.result = self.result[:expr.start] + change_to + self.result[endif_match.end():]
        elif type(expr) == Template.FORExpression:
            pass

    def _handle_csrf(self, match: Match[str]) -> None:
        self.result = self.result.replace(
            match.group(0),
            MakeCSRFProtectionToken()
        )

    def _handle_foreach(self, match: Match[str], for_variables: str, in_iterable: str) -> None:
        for_variables = for_variables.replace(" ", "")
        self.statement_stack.append(Template.FORExpression(
            match.start(0),
            for_variables.split(','),
            self._handle_generic_variable(in_iterable)))
        self.result = self.result.replace(
            match.group(0),
            "",
            1
        )
