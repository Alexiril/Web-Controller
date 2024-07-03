from http.server import ThreadingHTTPServer
from ssl import SSLContext
from typing import Any
from core.Config import read_config
from core.Handler import Handler
class Server(ThreadingHTTPServer):

    
    def __init__(self) -> None:
        server_conf = read_config("Server", dict[str, Any])
        bind_address = server_conf.get("bind-domain", "localhost")
        bind_port = server_conf.get("bind-port", 80)
        super().__init__((bind_address, bind_port), Handler)
        print(f"\033[92mServer with site '{server_conf.get('site-name', 'Web controller')}' started at ({bind_address}:{bind_port}).\033[0m")
        if server_conf.get("use-ssl", False):
            context = SSLContext()
            context.load_cert_chain(server_conf.get("ssl-cert", ""), server_conf.get("ssl-key", ""))
            self.socket = SSLContext().wrap_socket(sock=self.socket, server_side = True)
            
    def run(self) -> None:
        self.serve_forever()