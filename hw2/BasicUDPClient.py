# Park Yesol
# 20172129
# BasicUDPClient.py

from socket import *
from datetime import datetime

serverName = 'nsl2.cau.ac.kr'
serverPort = 32129

# Packet Structure [ option | message ]
class Option_Packet :
        def __init__(self, packet) :
                packet = str(packet)
                self.option = packet[0]
                self.message = packet[1:]

def option_menu() :
        print("============= <Menu> =============")
        for i in menu:
                print(i)

        option = input('Input option: ')
        return option

def get_millis(start, end):
	dt = end - start
	ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
	return ms

def UDP_communication(packet):
        sent_time = datetime.now()
        clientSocket.sendto(packet.encode(), (serverName, serverPort))
        # Receive
        receivePacket, serverAddress = clientSocket.recvfrom(2048)
        receive_time = datetime.now()
        response_time = float(get_millis(sent_time, receive_time))
        un_packet = Option_Packet(receivePacket.decode()) 

        print('Reply from server:', un_packet.message)
        print('Response time: {:.2f} ms'.format(response_time))

menu = ['1) convert text to UPPER-case',\
        '2) get my IP address and port number',\
        '3) get server time',\
        '4) get server running time',\
        '5) exit']


clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(('', 5432))

print("The client is running on port", clientSocket.getsockname()[1])

# Ctrl + C (KeyboardInterrupt)
try:
        while True : 
                option = option_menu()
                if option == '1':
                        message = input('Input lowercase sentence: ')
                        # Send with Option
                        packet = option + message
                        UDP_communication(packet)
        
                elif (option == '2' or option == '3' or option == '4'):
                        # No message. Only send Option
                        packet = option
                        UDP_communication(packet)

                elif option == '5':
                        packet = option
                        clientSocket.send(packet.encode())
                        print("The Client Program Exited")
                        break

                else :
                        print("Invalid Option Number Selected!")  

except KeyboardInterrupt:
        print('Bye bye~')

clientSocket.close()