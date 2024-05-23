from argParser import Arguments
from mainServer import ThreadedHTTPServer, Handler

if __name__ == "__main__":
    arguments = Arguments()
    ip_addr = arguments.get_arg('host')
    port = arguments.get_arg('port')

    # init server
    server = ThreadedHTTPServer((ip_addr, port), Handler)
    server.serve_forever()