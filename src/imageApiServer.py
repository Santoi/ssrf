import json
from socketserver import ThreadingMixIn
from urllib.parse import urlparse

from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    contentRoot = "."

    # perhaps replace with a database
    with open('../map.json', 'r') as file:
        imgLocation = json.load(file)
        print(imgLocation)


    # answers get request
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path != "/":
            self.send_error(404, "Path not found")
            self.end_headers()
            
        data_path = "./data.json"
        try:
            file_data = self.__retrieve_data(data_path)
            file_data_len = len(file_data)
        except Exception as ex:
            print ("Runtime Error: ", ex)
            self.send_error(404)
            self.end_headers()
            self.wfile.write(bytes("File not found",'utf-8'))
            return

        self.send_response(200)
        self.send_header("Content-Length",file_data_len)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(file_data)

    
    # returns all data from a file
    # same here, perhaps replace with db
    def __retrieve_data(self,path):
        data_path = self.__class__.contentRoot + path
        try:
            file = open(data_path,"rb")
        except IOError as ioerr:
            print ("File not found : ",ioerr)
        else:
            file_data = file.read()
            file.close()
        return file_data
    
    def parse_query(self, query):
        print(query)
        fields = {}
        for kv in query.decode('utf-8').split('&'):
            k, v = kv.split('=')
            fields[k] = v
        return fields
    


class ThreadedHTTPServer(ThreadingMixIn,HTTPServer):
    """ handles requests in separate threads """
    # ver como lograr que con CTRL + C no se rompa todo sino que termine bien
    # el codigo del otro server no nos sirve ni tampoco el original al tener multiples hilos
