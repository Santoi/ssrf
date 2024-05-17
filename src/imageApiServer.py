import cgi
import json
from socketserver import ThreadingMixIn
from urllib.parse import urlparse

from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    contentRoot = "."

    # perhaps replace with a database
    with open('../map.json', 'r') as file:
        imgLocation = json.load(file)

    # answers get request
    def do_GET(self):
        parsed_path = urlparse(self.path)

        # could be more object oriented but not feeling like it,
        # wont add any more endpoints ever
        if parsed_path.path != "/" and parsed_path.path != "/image":
            self.send_error(404, "Path not found")
            self.end_headers()
        
        self.respond_request(parsed_path)
    
    def respond_request(self, parsed_path):
        if parsed_path.path == "/":
            try:
                file_data, content_type = self.get_all_images()
            except Exception as ex:
                # couldnt open data file
                return self.handle_exception(500, ex)
        else:
            try:
                file_data, content_type = self.get_single_image(self.__parse_query(parsed_path.query))
            except Exception as ex:
                # couldnt find image asked by user, or forgot to ask for a certain id
                return self.handle_exception(404, ex)

        self.send_header("Content-Length", len(file_data))
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(file_data)

    def get_single_image(self, queryParams): 
        file_data = self.__retrieve_image(queryParams)
        self.send_response(200)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Disposition","attachment")

        return file_data, "image/jpeg"

    def get_all_images(self):
        self.send_response(200)
        return self.__retrieve_data("./data.json"), "application/json"

    def handle_exception(self, error_code, exception):
        self.send_error(error_code)
        self.end_headers()
        self.wfile.write(bytes(f"{exception}",'utf-8'))

    # returns all data from a file
    # same here, perhaps replace with db
    def __retrieve_data(self, path):
        data_path = self.__class__.contentRoot + path
        try:
            file = open(data_path,"rb")
            file_data = file.read()
            file.close()
            return file_data
        except:
            raise Exception("Something went wrong")

    # returns all bytes from an image file stored locally
    def __retrieve_image(self, queryParams):
        try: 
            url_path = self.imgLocation[queryParams['id']]
            image_path =  "./images/" + url_path
            file = open(image_path,"rb")
            file_data = file.read()
            file.close()
            return file_data
        except:
            raise Exception("Image could not be retrieved")
    
    def __parse_query(self, query):
        fields = {}
        for kv in query.split('&'):
            k, v = kv.split('=')
            fields[k] = v
        return fields


class ThreadedHTTPServer(ThreadingMixIn,HTTPServer):
    """ handles requests in separate threads """
    # ver como lograr que con CTRL + C no se rompa todo sino que termine bien
    # el codigo del otro server no nos sirve ni tampoco el original al tener multiples hilos
