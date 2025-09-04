from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def run_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", ".", perm="elradfmw")
    authorizer.add_anonymous(".")

    handler = FTPHandler
    handler.authorizer = authorizer

    # 使用非特权端口 2121
    server = FTPServer(("0.0.0.0", 2121), handler)

    server.serve_forever()

if __name__ == "__main__":
    run_ftp_server()