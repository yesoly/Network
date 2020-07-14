# Park Yesol
# 20172129
# MultiThreadTCPServer.py

from socket import *
from _thread import *
import threading
import time

# Packet Structure [ option | message ]
class Option_Packet :
    def __init__(self, packet) :
        packet = str(packet)
        self.option = packet[0]
        self.message = packet[1:]

class Client :
    def __init__(self, addr) :
        global client_num
        self.num = client_num
        self.ip = addr[0]
        self.port = addr[1]
        client_list.append(self)
        

serverPort = 32129
client_list = [] # Save Client Info
client_num = 1  # Client1, Client2, ... 

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()

print("The server is ready to receive on port", serverPort)
running_start = time.time()
    
def send_socket (option, message, clientSocket) :
    packet = option + message
    clientSocket.send(packet.encode())

def time_calculate(start, end):
    time_taken = end - start # time_taken is in seconds
    hours, rest = divmod(time_taken,3600)
    minutes, seconds = divmod(rest, 60)

    return hours, minutes, seconds

def connection_check(addr):
    global client_num
    isConnect = False
    for client in client_list :
        if client.port == addr[1] :
            isConnect = True
            number = client.num
            break
    if isConnect == False :
        Client(addr)
        number = client_num
        client_num += 1
    
    return number

def delete_list(addr):
    for client in client_list :
        if client.port == addr[1] :
            i = client_list.index(client)
            del client_list[i]

def check_client_num():
    while True:
        end = time.time() 
        H, M, S = time_calculate(running_start, end)
        
        if S == 0 :
            print("run time =  %02d:%02d:%02d" %(H, M, S)) 
            print("Number of connected clients ", len(client_list))


def thread_func(clientSocket, addr):
    num = connection_check(addr) # thread is new? current?
    print("Client ", num, ': connected. Number of connected clients' , len(client_list))

    while True: 
        receivePacket = clientSocket.recv(2048)
        
        if len(receivePacket) == 0:
            delete_list(addr)
            print("Client ", num,': disconnected. Number of connected clients', len(client_list))
            clientSocket.close()
            break

        un_packet = Option_Packet(receivePacket.decode())

        if un_packet.option == '1':
            print('Command ', un_packet.option)
            message = un_packet.message.upper()
            send_socket('1', message, clientSocket)
    
        elif un_packet.option == '2':
            print('Command ', un_packet.option)
            message = 'Reply from server: IP = {} , port = {}'.format(addr[0], addr[1])
            send_socket('2', message, clientSocket)

        elif un_packet.option == '3':
            print('Command ', un_packet.option)
            # current time on the server
            now = time.localtime()
            message = 'Reply from server: time = %02d:%02d:%02d' %(now.tm_hour, now.tm_min, now.tm_sec)
            send_socket('3', message, clientSocket)

        elif un_packet.option == '4':
            print('Command ', un_packet.option)
            # running time
            running_end = time.time()
            H, M, S = time_calculate(running_start, running_end)
            message = 'Reply from server: run time =  %02d:%02d:%02d' %(H, M, S)
            send_socket('4', message, clientSocket)

        elif un_packet.option == '5':
            print('Command ', un_packet.option)
            delete_list(addr)
            print("Client ", num, " disconnected. Number of connected clients ", len(client_list))
            clientSocket.close()
            break

        else:
            break

# this is initial code

try:
    start_new_thread(check_client_num,())
    while True :
        clientSocket, clientAddress = serverSocket.accept()
        start_new_thread(thread_func, (clientSocket, clientAddress))
        
except KeyboardInterrupt:
    print('Bye bye~')
    serverSocket.close()

serverSocket.close()



