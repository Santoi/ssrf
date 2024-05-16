import concurrent.futures
import socket

class Server:
    _BUFSIZE = 10000

    def __init__(self, address: str, port: str):
        self._skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._address = (address, port)
        self._skt.bind(self._address)
        self._active_clients = []

    def run(self):
        print("Server listening in " + self._address[0] + ":" + str(self._address[1]))
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                # Receive incoming messages and submit them to the thread pool
                data, addr = self._skt.recvfrom(self._BUFSIZE)
                future = executor.submit(self.handle_request, data, addr)
                future.add_done_callback(lambda f: f.result())

    def handle_request(self, data, client_addr):
        pass


