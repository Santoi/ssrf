from socketserver import ThreadingMixIn
from urllib.parse import urlparse

__author__ = 'rudolph'

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import threading

class GetPostHandler(BaseHTTPRequestHandler):

    contentRoot = "./images"
    uploadUrlPath = "/files"
    def do_GET(self):
        print("doGet called")
        print (threading.currentThread().getName())

        parsed_path = urlparse(self.path)
        print (parsed_path.path)
        try:
            file_data = self.__retrieve_image(parsed_path.path)
            file_data_len = len(file_data)

        except Exception as ex:
            print ("Runtime Error: ", ex)
            self.send_error(404)
            self.end_headers()
            self.wfile.write(bytes("File not found",'utf-8'))
            return
        else:
            content_type = self.__find_out_content_type(parsed_path.path)
            print (content_type)
            self.send_response(200)
            self.send_header("Accept-Ranges","bytes")
            self.send_header("Content-Disposition","attachment")
            self.send_header("Content-Length",file_data_len)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(file_data)

        return



    def __find_out_content_type(self,url_path):
        pieces = url_path.rsplit(".", 1)
        print (pieces)
        file_extention = pieces[1]
        if file_extention == "gif":
            return "image/gif"
        elif file_extention in ["jpeg","jpe","jpg", "jif","jfif","jfi"]:
            return "image/jpeg"
        elif file_extention == "png":
            return "image/png"
        elif file_extention in ["svg", "svgz"]:
            return "image/svg+xml"
        elif file_extention in ["tiff","tif"]:
            return "image/tiff"
        elif file_extention == ".ico":
            return "image/vnd.microsoft.icon"
        elif file_extention == ".wbmp":
            return "image/vnd.wap.wbmp"
        else:
            return "text/plain"



    def __retrieve_image(self,url_path):
        image_path = self.__class__.contentRoot + url_path
        try:
            file = open(image_path,"rb")
        except IOError as ioerr:
            print ("File not found : ",ioerr)
        else:
            file_data = file.read()
            file.close()
        return file_data

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={ 'REQUEST_METHOD' : 'POST',
                      'CONTENT_TYPE' : self.headers['Content-Type'],
            })

        response_msg = None
        
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # field contains an uploaded file
                print( "\n ********** \n")
                print (field_item.filename)
                file_data = field_item.file.read()
                file_len = len(file_data)
                print (file_len)
                try:
                    self.__save_image(file_data)
                except Exception as ex:
                    print ("Runtime Error: ", ex)
                    self.send_error(500)
                    self.end_headers()
                    self.wfile.write("Can not upload file to server")
                    return
                else:
                    response_msg = "File uploaded"
            else:
                # regular form value
                self.wfile.write('\t%s=%s\n' % (field, form[field].value))

        # building successful response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response_msg)

        return




    def __save_image(self,file_data):
        parsed_path = urlparse(self.path)

        import os
        path_to_upload_file = self.__class__.contentRoot + parsed_path.path
        result = path_to_upload_file.rsplit("/",1)
        print (result)
        path_to_create_dir = result[0]
        try:
            os.makedirs(path_to_create_dir)
        except OSError as oserror:
            print ("Error while creation path to upload file ", oserror)

        try:
           file = open(path_to_upload_file,"wb")
        except IOError as ioerror:
            print( "Can not open file: ", ioerror)
            raise Exception("Can not save file on server",)
        else:
            file.write(file_data)
            file.close()
            print ("file closed")

        return


class ThreadedHTTPServer(ThreadingMixIn,HTTPServer):
    """ handles requests in separate threads """


if __name__ == "__main__":
    print ("Hello Server : ")

    server = ThreadedHTTPServer(('localhost',8080),GetPostHandler)
    print ("Starting server, use Ctrl+C to stop")
    server.serve_forever()
