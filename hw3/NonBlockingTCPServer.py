# Park Yesol
# 20172129
# NonBlockingTCPServer.py

from socket import *
from select import *
import time

serverPort = 32129
clients = {} # Save Client Info
client_num = 1  # Client1, Client2, ...

# Packet Structure [ option | message ]
class Option_Packet :
    def __init__(self, packet) :
        packet = str(packet)
        self.option = packet[0]
        self.message = packet[1:]


def send_socket (option, message, socket) :
    packet = option + message
    socket.send(packet.encode())

def time_calculate(start, end):
    time_taken = end - start # time_taken is in seconds
    hours, rest = divmod(time_taken,3600)
    minutes, seconds = divmod(rest, 60)

    return hours, minutes, seconds

def check_client_num():
    end = time.time() 
    H, M, S = time_calculate(running_start, end)
    if ((S // 1) % 60) == 0 :
        print("run time =  %02d:%02d:%02d" %(H, M, S)) 
        print("Number of connected clients ", len(select_list)-1)


def check_number(socket):
    for i, value in clients.items() : 
        if value == socket :
            return i
    return -1

try:
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen()
    select_list =[serverSocket]

    print("The server is ready to receive on port", serverPort)
    running_start = time.time()

    while select_list :
        # wait to receive packet
        check_client_num()    
        read_socket, write_socket, error_socket = select(select_list, [], [], 1) 
        
        for socket in read_socket:
            if socket == serverSocket:
                (clientSocket, clientAddress) = socket.accept()
                select_list.append(clientSocket)
                clients[client_num] = clientSocket
                print("Client ",client_num, " connected. Number of connected clients ", len(select_list)-1)
                client_num += 1

            else :
                receivePacket = socket.recv(2048)
                num = check_number(socket)
            
                if len(receivePacket) == 0:
                    select_list.remove(socket)
                    clients.pop(num, None)
                    print("Client ", num, " disconnected. Number of connected clients ", len(select_list)-1)
                    socket.close()
                    break 
              
               	un_packet = Option_Packet(receivePacket.decode())

               	if un_packet.option == '1':
                    print('Command ', un_packet.option)
                    message = un_packet.message.upper()
                    send_socket('1', message, socket)
    
                elif un_packet.option == '2':
                    print('Command ', un_packet.option)
                    message = 'Reply from server: IP = {} , port = {}'.format(clientAddress[0], clientAddress[1])
                    send_socket('2', message, socket)

                elif un_packet.option == '3':
                    print('Command ', un_packet.option)
                    # current time on the server
                    now = time.localtime()
                    message = 'Reply from server: time = %02d:%02d:%02d' %(now.tm_hour, now.tm_min, now.tm_sec)
                    send_socket('3', message, socket)

                elif un_packet.option == '4':
                    print('Command ', un_packet.option)
                    # running time
                    running_end = time.time()
                    H, M, S = time_calculate(running_start, running_end)
                    message = 'Reply from server: run time =  %02d:%02d:%02d' %(H, M, S)
                    send_socket('4', message, socket)

                elif un_packet.option == '5':
                    print('Command ', un_packet.option)
                    select_list.remove(socket)
                    clients.pop(num, None)
                    print("Client ", num, " disconnected. Number of connected clients ", len(select_list)-1)
                    socket.close()
                   

except KeyboardInterrupt:
    print('Bye bye~')
    serverSocket.close()
   

serverSocket.close()