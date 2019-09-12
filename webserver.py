# -*- coding: utf-8 -*-

import os
import thread
import socket

class WebServer:
    def main(self):
        port = 1234
        host = 'localhost'
        
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind((host, port))
        tcp.listen(1)

        while True:
            (con, (ip, porta)) = tcp.accept()
                
            request = HttpRequest(con)
            thread.start_new_thread(request.run, ())
                
class HttpRequest():
    def __init__(self, request_socket):
        self.request_socket = request_socket
        self.CRLF = "\r\n"

    def run(self):
        try:
            self.processRequest()
        except:
            print "Falha na execucao"

    def processRequest(self):
        input_stream = self.request_socket.recv(1024)

        request_line = input_stream.split(self.CRLF)[0]

        print request_line
        file_name = request_line.split(" ")[1]
        file_name = os.getcwd() + file_name

        file_exists = True
        if(os.path.isfile(file_name)):
            fis = open(file_name, "rb")
        else:
            file_exists = False

        status_line = ""
        content_type_line = ""
        entity_body = ""
        
        if(file_exists):
            status_line = "0"
            content_type_line = "Content-type: " + self.contentType(file_name) + self.CRLF

        else:
            status_line = "404 Not Found"
            content_type_line = "text/html"
            entity_body = "<HTML>" + "<HEAD><TITLE>Not Found</TITLE></HEAD>" + "<BODY>Not Found</BODY></HTML>"

        self.request_socket.send(status_line)
        self.request_socket.send(content_type_line)
        self.request_socket.send(self.CRLF)

        if(file_exists):
            file_piece = fis.read(1024)
            while(file_piece):
                self.request_socket.send(file_piece)
                file_piece = fis.read(1024)

            fis.close()

        else:
            self.request_socket.send(entity_body)

        self.request_socket.close()
    
    def contentType(self, file_name):
        file_end = file_name.split(".")[-1]
        if (file_end == "htm" or file_end == "html"):
            return "text/html"

        return "application/octet-stream"


if __name__ == '__main__':
    server = WebServer()
    server.main()