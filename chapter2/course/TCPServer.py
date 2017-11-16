from socket import *

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('the server is ready to receive')

while 1:
    connectionSocket, addr = serverSocket.accept()
    message, dd = connectionSocket.recvfrom(2048)

    print('receive' + str(message))
    message_upper = message.upper()

    connectionSocket.send(message_upper)
