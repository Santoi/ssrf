from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import requests
from urllib.parse import urlparse

class Handler(BaseHTTPRequestHandler):

    # change back to post, but set get so as to be able to access via internet
    def do_GET(self):
        parsed_path = urlparse(self.path)
        print(parsed_path)
        # could be more object oriented but not feeling like it,
        # wont add any more endpoints ever
        if parsed_path.path != "/secret" and parsed_path.path != "/image":
            self.send_error(404, "Path not found")
            self.end_headers()

        if parsed_path.path == "/image":
            self.handle_image_req()
        else:
            self.handle_secret()

    def handle_image_req(self):
        # read the body of the request
        if 'Content-Length' not in self.headers:
            self.send_user_error(b'Incomplete request: something in request body is missing')
            return 
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        print(post_data)
        
        # only allows your request if you have "urlToRedirect=url" as 
        # this server does not handle images 
        prefix = "urlToRedirect="
        if post_data.startswith(prefix):
            # extracts value of urlToRedirect field (awfully but works)
            url_to_redirect = post_data.split('\n', 1)[0].replace(prefix, "").replace('"', "").strip()
            print(url_to_redirect)
            try:
                response = requests.get(url_to_redirect)
                # resend 
                self.send_response(response.status_code)
                if 'Content-type' in  response.headers:
                    self.send_header('Content-type', response.headers['Content-Type'])
                self.end_headers()
                self.wfile.write(response.content)

            except requests.RequestException as e:
                # could not do get request properly
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'Error fetching URL: {e}'.encode('utf-8'))
        
        else:
            self.send_user_error(b'Missing a url to request images')
            
    def send_user_error(self, msg):
        self.send_response(400)
        self.end_headers()
        self.wfile.write(msg)

    def handle_secret(self):
        # endpoint should not be accesible if not in LAN

        # if has a forwarded host, then comes from ngrok tunel
        if 'X-Forwarded-Host' not in self.headers:
            print("hacked")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Dang it, you hacked me!!')
        else:
            print("firewalled")
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'Forbidden')
    
class ThreadedHTTPServer(ThreadingMixIn,HTTPServer):
    """ handles requests in separate threads """
    # ver como lograr que con CTRL + C no se rompa todo sino que termine bien
    # el codigo del otro server no nos sirve ni tampoco el original al tener multiples hilos
