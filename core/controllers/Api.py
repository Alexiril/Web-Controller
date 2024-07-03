from json import JSONDecoder, JSONEncoder
from core.Exceptions import LockObjectException
from core.controllers.api_requests.Application import ApplicationRequest, GetApplications
from core.controllers.api_requests.Auth import MakeAuthTokenApiRequest
from core.Controller import Controller


class ApiController(Controller):

    def __call__(self, handler, arguments, user) -> bytes:
        req = arguments[0]
        cont_len = int(handler.headers.get('content-length', 0))
        data = handler.rfile.read(cont_len).decode()
        data = JSONDecoder().decode(data if data != "" else "{}")
        result = ""
        handler.reactive_headers["Content-Type"] = "application/json"
        try:
            match req:
                case "get-token":
                    result = MakeAuthTokenApiRequest(
                        handler,
                        "POST",
                        {"user", "key"},
                        user,
                        data,
                        True
                    )()
                case "get-apps":
                    result = GetApplications(
                        handler,
                        "GET",
                        set(),
                        user,
                        {},
                        needs_user=True
                    )()
                case "app-request":
                    result = ApplicationRequest(
                        handler,
                        "POST",
                        {"appid", "command", "data"},
                        user,
                        data,
                        needs_user=True
                    )()
        except LockObjectException as e:
            handler.reactive_response = getattr(e.evalue, 'response', 500)
            return JSONEncoder().encode({
                "result": "error",
                "cause": str(e.evalue),
                "ecode": str(getattr(e.evalue, 'ecode', 0))
            }).encode()
        except Exception as e:
            handler.reactive_response = getattr(e, 'response', 500)
            return JSONEncoder().encode({
                "result": "error",
                "cause": str(e),
                "ecode": str(getattr(e, 'ecode', 0))
            }).encode()
        return JSONEncoder().encode({
            "result": "done",
            "value": result
        }).encode()
