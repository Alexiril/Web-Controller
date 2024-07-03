from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from typing import Any
from core.Config import read_config
from core.User import auth_user
from core.Exceptions import log_exception
from core.Router import router
from core.controllers.Error import ErrorController

class Handler(BaseHTTPRequestHandler):

    
    def __init__(self, request, client_address, server) -> None:
        self.output: bytes = b""
        self.server_settings = read_config("Server", dict[str, Any])
        is_https = self.server_settings.get('use-ssl', False)
        domain = self.server_settings.get('bind-domain', 'localhost')
        port = self.server_settings.get('bind-port', 80)
        self.reactive_headers: dict[str, str] = {
            "Content-Type": "text/html",
            "Server": self.server_settings.get("server-name", "Web controller"),
            'Date': self.date_time_string(),
            'Access-Control-Allow-Origin': f"http{'s' if is_https else ''}://{domain}:{port}"
        }
        self.reactive_response: int = HTTPStatus.OK.value
        super().__init__(request, client_address, server)

    def do_request(self, do_send_output: bool) -> None:
        user = auth_user(self)
        try:
            with router as _router:
                self.output = _router.route(self, self.path, user)
        except Exception as exception:
            try:
                self.output = ErrorController(exception)(self, (), user)
            except Exception:
                self.output = b""
            log_exception(exception)
        if self.output != None:
            self.reactive_headers["Content-Length"] = str(len(self.output))
        if self.server_settings.get("log-requests", True):
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