from http.server import ThreadingHTTPServer
from ssl import wrap_socket, PROTOCOL_TLS
from core.Handler import Handler
from core.Config import SERVER

class Server(ThreadingHTTPServer):

    def __init__(self) -> None:
        bind_address = SERVER.get("bind-ip", "localhost")
        bind_port = SERVER.get("bind-port", 80)
        super().__init__((bind_address, bind_port), Handler)
        print(f"\033[92mServer with site '{SERVER.get('site-name', 'Web controller')}' started at ({bind_address}:{bind_port}).\033[0m")
        if SERVER.get("use-ssl", False):
            self.socket = wrap_socket(
                sock=self.socket,
                server_side = True,
                certfile = SERVER.get("ssl-cert", ""),
                keyfile = SERVER.get("ssl-key", ""),
                ssl_version = PROTOCOL_TLS
                )
            
    def run(self) -> None:
        self.serve_forever()