# -*- coding: utf-8 -*-
from socket import *
import threading
import datetime

CRLF = "\r\n"
BLANK = " "
STATUS_CODE_MSG = {200: 'OK', 404: 'NOT FOUND', 500: 'SERVER ERROR'}


class Server:
    def __init__(self, server_name, port) -> None:
        self.server_name = server_name
        self.port = port
        self.showdown = False

    def start(self):
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(('', self.port))
        server_socket.listen(1)
        print('server start at ' + str(self.port))

        self.receive(server_socket)

    def receive(self, server_socket):
        while not self.showdown:
            connection_socket, addr = server_socket.accept()
            thread = threading.Thread(target=Dispatcher, args=(connection_socket, addr, self.server_name))
            thread.start()


class Dispatcher:
    def __init__(self, connection_socket, addr, server_name) -> None:
        print("客户端连接　==>> ip:" + str(addr[0]) + " ,port: " + str(addr[1]))

        request = Request(connection_socket.recvfrom(2048)[0])

        print(request.request_info)
        print(request.method)
        print(request.context_path)
        response = Response(connection_socket, server_name, 'text/html; charset=utf-8')
        response.print(200, "<h1>Hello fuckServer</h1><br>" + str(request.params))


class Request:
    def __init__(self, request_row) -> None:
        self.request_info = request_row.decode()
        print(self.request_info)
        self.method = ""
        self.context_path = ""
        self.params = {}
        self.parse_request_line()

    def parse_request_line(self):
        request_lines = self.request_info.split(CRLF)
        first_lines = request_lines[0].split(BLANK)
        self.method = first_lines[0]

        print(self.method)

        path_parameters = first_lines[1].split("?")
        self.context_path = path_parameters[0]

        if len(path_parameters) > 1:
            self.parse_parameters(path_parameters[1])

        head_data = self.request_info.split(CRLF + CRLF)
        if len(head_data) > 1:
            self.parse_parameters(head_data[1])

    def parse_parameters(self, parameters_str):
        if parameters_str.strip() == "":
            return

        print('try parse ==>> ' + parameters_str)
        params_values = parameters_str.split("&")
        for param_str in params_values:
            param_val = param_str.split("=")
            self.params[param_val[0]] = param_val[1]


class Response:
    def __init__(self, connection_socket, server_name, content_type) -> None:
        self.connection_socket = connection_socket
        self.server_name = server_name
        self.content_type = content_type
        self.head = ""
        self.content_length = 0

    def create_head(self, code):
        self.head = "HTTP/1.1" + BLANK + str(code) + BLANK + STATUS_CODE_MSG[code] + CRLF \
                    + "Server:" + self.server_name + CRLF \
                    + "Date:" + str(datetime.datetime.now().strftime('%a, %d %b %y %H:%M:%S GMT')) + CRLF \
                    + "Content-Type:" + self.content_type + CRLF \
                    + "Content-Length:" + str(self.content_length) + CRLF + CRLF

    def print(self, code, content):
        self.content_length = len(content.encode('utf-8'))
        self.create_head(code)
        encode = (self.head + content).encode('utf-8')

        print("-----------------------------------")
        print('send == > ' + str(encode))
        self.connection_socket.send(encode)


if __name__ == '__main__':
    server = Server('fuckServer', 9999)
    server.start()
