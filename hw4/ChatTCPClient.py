# Park Yesol
# 20172129
# ChatTCPClient.py

from socket import *
from threading import Thread
from datetime import datetime
from datetime import timedelta
import sys

CLIENT_ver = "2.0"

serverName = "nsl2.cau.ac.kr"
serverPort = 22129

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((serverName, serverPort))
sent_time = 0

try :
    username = sys.argv[1]
except IndexError :
    print("Index Error")
    os._exit(0)

def get_millis(start, end):
    dt = end - start
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds/1000.0
    f_ms = float(ms)
    print('>> Response time: {:.2f} ms'.format(f_ms))

def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)

            if not message:
                break
            elif message.decode().strip() == '\\adios~':
                print('adios~')
                client_socket.close()
                sys.exit()
                break
            elif message.decode().strip() == '\\rtt':
                receive_time = datetime.now()
                get_millis(sent_time, receive_time)
                continue

            print(message.decode())

        except:
            pass

def run_chat_thread():
    thread = Thread(target = receive_message, args = (client_socket,))
    thread.daemon = True
    thread.start()
    
    print("==== The thread is connected. You are ready for communications. Client Version " + CLIENT_ver + " ====")
    init = CLIENT_ver + " " + username
    client_socket.send(init.encode())

    while True:
        try:
            message = input()

            if message.strip() == '\\rtt':
                global sent_time
                sent_time = datetime.now()
            
            client_socket.send(message.encode())

        except KeyboardInterrupt:
            message = '\\exit'
            client_socket.send(message.encode())
            print('adios~')
            client_socket.close()
            sys.exit()
                
run_chat_thread()

        