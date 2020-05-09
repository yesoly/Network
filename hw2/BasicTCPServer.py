# Park Yesol
# 20172129
# BasicTCPServer.py

from socket import *
import time


# Packet Structure [ option | message ]
class Option_Packet :
    def __init__(self, packet) :
        packet = str(packet)
        self.option = packet[0]
        self.message = packet[1:]

serverPort = 32129
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

def send_socket (option, message) :
    packet = option + message
    connectionSocket.send(packet.encode())

def time_calculate(start, end):
    time_taken = end - start # time_taken is in seconds
    hours, rest = divmod(time_taken,3600)
    minutes, seconds = divmod(rest, 60)

    return hours, minutes, seconds

print("The server is ready to receive on port", serverPort)
running_start = time.time()


try :
    while True:
        (connectionSocket, clientAddress) = serverSocket.accept()
        print('Connection requested from', clientAddress)

        # wait to receive packet
        while(True):
            receivePacket = connectionSocket.recv(2048)
            if len(receivePacket) == 0:
                print('Server is closed T.T')
            un_packet = Option_Packet(receivePacket.decode())

            if un_packet.option == '1':
                print('Command ', un_packet.option)
                message = un_packet.message.upper()
                send_socket('1', message)
    
            elif un_packet.option == '2':
                print('Command ', un_packet.option)
                message = 'Reply from server: IP = {} , port = {}'.format(clientAddress[0], clientAddress[1])
                send_socket('2', message)

            elif un_packet.option == '3':
                print('Command ', un_packet.option)
                # current time on the server
                now = time.localtime()
                message = 'Reply from server: time = %02d:%02d:%02d' %(now.tm_hour, now.tm_min, now.tm_sec)
                send_socket('3', message)

            elif un_packet.option == '4':
                print('Command ', un_packet.option)
                # running time
                running_end = time.time()
                H, M, S = time_calculate(running_start, running_end)
                message = 'Reply from server: run time =  %02d:%02d:%02d' %(H, M, S)
                send_socket('4', message)

            elif un_packet.option == '5':
                print('Command ', un_packet.option)
                connectionSocket.close()
                break

except KeyboardInterrupt:
    print('Bye bye~')

connectionSocket.close()
serverSocket.close()
