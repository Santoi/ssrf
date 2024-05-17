import argparse
import netifaces as ni

class Arguments:
    def __init__(self):
        self._args = self.__parse()

    def __parse(self):
        parser = argparse.ArgumentParser(description='Main server commands')
        parser.add_argument(
        "-H", "--host", default=self._ip_default(), help="server IP address")
        parser.add_argument(
        "-p", "--port", type=int, default="9090", help="server port")
        
        return parser.parse_args()

    def get_args(self):
        return self._args

    def get_arg(self, arg):
        map = vars(self.get_args())
        return map[arg]
    
    # Set default IP address as localhost.
    def _ip_default(self):
        interfaces = ni.interfaces()
        i = [interface for interface in interfaces if 'eth0' in interface]
        if len(i) > 0:
            ip = ni.ifaddresses(i[0])[ni.AF_INET][0]['addr']
        else:
            ip = "127.0.0.1"    
        return ip
