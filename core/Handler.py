from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from core.Exceptions import log_exception
from core.Router import get_router
from core.Config import SERVER
from core.controllers.Error import ErrorController

class Handler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server) -> None:
        self.output: bytes = b""
        self.reactive_headers: dict[str, str] = {
            "Content-Type": "text/html",
            "Server": SERVER.get("server-name", "Web controller"),
            'Date': self.date_time_string()
        }
        self.reactive_response: int = HTTPStatus.OK.value
        super().__init__(request, client_address, server)

    def do_request(self, do_send_output: bool) -> None:
        try:
            self.output = get_router().route(self, self.path)
        except Exception as exception:
            try:
                self.output = ErrorController(exception)(self, ())
            except:
                self.output = b""
            log_exception(exception)
        if self.output != None:
            self.reactive_headers["Content-Length"] = str(len(self.output))
        if SERVER.get("log-requests", True):
            self.log_request(self.reactive_response)
        self.send_response_only(self.reactive_response)
        for header, value in self.reactive_headers.items():
            self.send_header(header, value)
        self.end_headers()
        if not do_send_output:
            return
        try:
            self.wfile.write(self.output)
        except Exception as exception:
            log_exception(exception)

    def do_GET(self) -> None:
        return self.do_request(True)
        
    def do_POST(self) -> None:
        return self.do_request(True)

    def do_HEAD(self) -> None:
        return self.do_request(False)