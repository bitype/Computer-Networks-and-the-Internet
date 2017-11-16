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

        print('+----------------------------------+')
        print(request.http_method)
        print(request.context_path)
        print(request.host)
        print('+----------------------------------+')

        try:
            # 建立连接
            http_sock = socket(AF_INET, SOCK_STREAM)
            http_sock.connect((request.host, 80))
            http_sock.sendall(request.request_info.encode())
            while True:
                http_data = http_sock.recv(1024)
                if http_data:
                    connection_socket.send(http_data)
                else:
                    break
            http_sock.close()
        except TimeoutError:
            print('|||||||||||||||||||||||||||||||')
            pass


class Request:
    def __init__(self, request_row) -> None:
        self.request_info = request_row.decode()
        self.http_method = ""
        self.context_path = ""
        self.host = ""
        self.port = 80
        self.params = {}
        self.parse_request_line()

    def parse_request_line(self):
        print('+======================================+')
        print(self.request_info)
        print('+======================================+')
        request_lines = self.request_info.split(CRLF)
        first_lines = request_lines[0].split(BLANK)
        self.http_method = first_lines[0]

        path_parameters = first_lines[1].split("?")
        self.context_path = path_parameters[0]
        host_port = self.context_path.replace('http://', '').split('/')[0].split(':')
        self.host = gethostbyname(host_port[0])
        if len(host_port) > 1:
            self.port = int(host_port[1])
        if len(path_parameters) > 1:
            self.parse_parameters(path_parameters[1])

        head_data = self.request_info.split(CRLF + CRLF)
        if len(head_data) > 1:
            self.parse_parameters(head_data[1])

    def parse_parameters(self, parameters_str):
        if parameters_str.strip() == "":
            return
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
