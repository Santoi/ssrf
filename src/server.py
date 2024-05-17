import concurrent.futures
import signal
import socket

class Server:
    _BUFSIZE = 10000

    def __init__(self, address: str, port: str):
        self._skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._address = (address, port)
        self._skt.bind(self._address)
        self._skt.listen()
        # Catch SIGINT
        self._activate_sigint_handler()
        self._active_clients = {}


    def run(self):
        print("Server listening in " + self._address[0] + ":" + str(self._address[1]))
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                # Receive incoming messages and submit them to the thread pool
                client_skt, addr = self._skt.accept()
                self._active_clients[addr] = client_skt
                future = executor.submit(self.handle_client, client_skt)
                future.add_done_callback(lambda f: f.result())

    def handle_client(self, client_skt):
        # TODO: handle request.
        data = client_skt.recv(self._BUFSIZE)
        # Close client connection after handling the request.
        client_skt.close()
        self._active_clients.remove(client_skt)

    def _activate_sigint_handler(self):
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self):
        res = input("Do you really want to exit? y/n ")
        if res == "y":
            for client in self._active_clients:
                client.close()
            self._skt.close()
            exit(1)

