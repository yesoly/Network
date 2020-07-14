# Park Yesol
# 20172129
# FileChatTCPClient.py

from socket import *
from threading import Thread
from datetime import datetime
from datetime import timedelta
import os
import sys
import time

CLIENT_ver = "2.0"
MB = 1024 * 1024
KB = 1024
FIN = '\\fin'

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
            message = message.decode()

            if not message:
                print('server connection is closed')
                client_socket.close()
                sys.exit()
                break

            if message[0] == '\\':
                msg_list = message.split(" ")
                if msg_list[0] == '\\adios~':
                    print('adios~')
                    client_socket.close()
                    sys.exit()
                    break

                elif msg_list[0] == '\\rtt':
                    receive_time = datetime.now()
                    get_millis(sent_time, receive_time)
                    print(message.decode())
                    continue

                # \\file new_file_name
                elif msg_list[0].strip() in '\\file':    
                    filename = msg_list[1]
                    filedata = b''
                    while True:
                        print('>> receving file ...')
                        f = client_socket.recv(1024)
                        if (f.decode() == '\\fin'):
                            print('------- finish receiving file -------')
                            break
                        filedata += f
                    
                    with open(filename, 'wb') as new_file:
                    	new_file.write(filedata)
                    	new_file.close()
                    	print('file is downloaded')                   
                    continue

                else:
                    print(there is not command)
                    continue
            else:
                print(message)

        except:
            pass

def run_chat_thread():
    thread = Thread(target = receive_message, args = (client_socket,))
    thread.daemon = True
    thread.start()
    print("==== The thread is connected. You are ready for communications. Client Version " + CLIENT_ver + " ====")
    init = CLIENT_ver + " " + username
    client_socket.send(init.encode('utf-8'))

    while True:
        try:
            message = input()

            if message[0] == '\\':
                msg_list = message.split(" ")
                if msg_list[0] == '\\fsend' or msg_list[0] == '\\wsend':
                    filename = msg_list[1]
                    if os.path.exists(filename):
                        with open(filename, 'rb') as f:
                            fdata = f.read()
                    
                        if len(fdata) > 5 * MB:
                            print("Too Big File size (Must under 5MB)")
                        else:
                            client_socket.send((message).encode())
                            while(len(fdata) > KB):
                                client_socket.send(fdata[:KB])
                                fdata = fdata[KB:]
                            client_socket.send(fdata)
                            time.sleep(0.1)
                            client_socket.send((FIN).encode())

                    else:
                        print("file does not exist")

                elif msg_list[0] == '\\rtt':
                    global sent_time
                    sent_time = datetime.now()
            else:
                client_socket.send(message.encode())

        except KeyboardInterrupt:
            message = '\\exit'
            client_socket.send(message.encode())
            print('adios~')
            client_socket.close()
            sys.exit()
                
run_chat_thread()

        