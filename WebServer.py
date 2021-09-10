#import socket module
from socket import *
import sys #In order to terminate the program
serverSocket = socket(AF_INET, SOCK_STREAM)
#prepare seerver socket
HOST = '127.0.0.1'
PORT = 65432
serverSocket.bind((HOST, PORT)) #binds host address and port together
serverSocket.listen()

while True:
    #establish connection
    print ('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        #send one HTTP header line into socket
        connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
        connectionSocket.send('Content-Type: text/html\n'.encode())

        #Send the content of the requested file to the client
        for i in range(-1, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close

    except IOError:
        #Send response message for file not found
        f = open("404message.html")
        outputdata = f.read()
        #send one HTTP header line into socket
        connectionSocket.send('HTTP/1.0 404 OK\n'.encode())
        connectionSocket.send('Content-Type: text/html\n'.encode())

        #Send the content of the requested file to the client
        for i in range(-1, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        #Close client socket
        connectionSocket.close

    serverSocket.close()
    sys.exit() #Terminate the program after sending the corresponding data