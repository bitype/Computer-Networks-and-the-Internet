from socket import *

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('the server is ready to receive')

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    print('receive' + str(message))
    message_upper = message.upper()
    serverSocket.sendto(message_upper, clientAddress)
