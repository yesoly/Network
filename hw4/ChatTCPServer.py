# Park Yesol
# 20172129
# ChatTCPServer.py

import socketserver
import threading

SERVER_ver = "1.1"
serverPort = 22129
lock = threading.Lock()

new_name_temp = ''

class User:
    def __init__(self):
        self.users = {}
        self.client_version = {}

    def nicknameCondition(self, nickname, conn):
        # Nickname Condition
        if nickname in self.users:
            conn.send('that nickname is used by another user. cannot connect.\n'.encode())
            return -1    
        for idx in nickname :
            if (not idx.isalpha() and idx != '-') :
                conn.send('Nicknames have to be written in English. and no spaces or special characters except dash [-].\n'.encode())
                return -1
        if len(nickname) > 32:
            conn.send('Nickname must be no more than 32 characters.\n'.encode())
            return -1
    
    def newUser(self, nickname, conn, addr, version):
        # Number of participants Condition
        if len(self.users) == 10:
            conn.send('full. cannot connect.\n'.encode())
            return None

        if self.nicknameCondition(nickname, conn) == -1:
            return None

        lock.acquire()
        self.users[nickname] = (conn, addr)
        self.client_version[nickname] = version
        lock.release()

        self.sendAll('[welcome %s to cau-cse chat room at %s %s. You are %dth user.]' %(nickname, addr[0], addr[1], len(self.users)))
        return nickname
        
    def removeUser(self, nickname):
        if nickname not in self.users:
            return
        lock.acquire()
        del self.users[nickname]
        lock.release()
            
        self.sendAll('[%s is disconnected. There are %d users in the chat room.]' %(nickname, len(self.users)))
            
    def messageHandler(self, nickname, msg):
        if msg[0] != '\\':
            self.sendExceptSender('%s> %s' %(nickname, msg), nickname)
            if 'i hate professor' in msg.lower():
                self.removeUser(nickname)
                return -1
            else:
                return

        if msg[0] == '\\':
            msg_list = msg.split(" ")
            if msg_list[0] == '\exit':
                self.removeUser(nickname)
                return -1
            # show all users
            elif msg_list[0] == '\\users':
                for key, value in self.users.items():
                    self.sendSender('users >> %s %s' %(key, value[1]), nickname)
                return
            # whistper
            elif msg_list[0] == '\\wh':
                if len(msg_list) < 3 :
                    self.sendSender('>> whisper command format is [\\wh <nickname> <message>]', nickname)
                else :
                    receiver = msg_list[1]
                    message = " ".join(msg_list[2:])
                    self.sendSender('whisper[%s] >> %s' %(nickname, message), receiver)
                return
            elif msg_list[0] == '\\version':
                self.sendSender('version >> CLIENT_VERSION %s / SERVER_VERSION %s' %(self.client_version[nickname], SERVER_ver), nickname)
                return
            elif msg_list[0] == '\\rename':
                new_name = msg_list[1]
                sender_conn, sender_addr = self.users[nickname]
                if (self.nicknameCondition(new_name, sender_conn) != -1):
                    lock.acquire()
                    self.sendSender('>>your nickname is changed. [%s] > [%s]' %(nickname, new_name), nickname)
                    self.users[new_name] = self.users[nickname]
                    global new_name_temp
                    new_name_temp = new_name
                    del self.users[nickname]
                    lock.release()
                return -2
            elif msg_list[0] == '\\rtt':
                self.sendSender('\\rtt', nickname)
                return

    def sendSender(self, msg, sender):
        sender_conn, sender_addr = self.users[sender]
        sender_conn.send(msg.encode())

    def sendExceptSender(self, msg, sender):
        sender_conn, sender_addr = self.users[sender]
        for conn, addr in self.users.values():
            if conn == sender_conn and addr == sender_addr:
                continue
            else:
                conn.send(msg.encode())
        
    def sendAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())


class SocketHandler(socketserver.BaseRequestHandler):
    user = User()
    
    def handle(self):
        try:
            global new_name_temp
            username = self.registerUsername()
            
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())
                handler_result = self.user.messageHandler(username, msg.decode())

                if handler_result == -1:
                    self.request.send('\\adios~'.encode())
                    self.request.close()
                    break
                if handler_result == -2:
                    username = new_name_temp

                msg = self.request.recv(1024)
                
        except Exception as e:
            print(e)
        
        print('%s left. There are %d users now.' %(username, len(self.user.users)))
        self.user.removeUser(username)
        
    def registerUsername(self):
        init_msg = self.request.recv(1024)
        init_msg = init_msg.decode()
        init_list = init_msg.split(" ")
        version = init_list[0]
        name = init_list[1]
        if self.user.newUser(name, self.request, self.client_address, version):
            print('%s joined. There are %d users connected.' %(name, len(self.user.users)))
            return name
        
        else:
            while True:      
                self.request.send('Nickname:'.encode())
                name = self.request.recv(1024)
                name = name.decode()
                if self.user.newUser(name, self.request, self.client_address, version):
            	    print('%s joined. There are %d users connected.' %(name, len(self.user.users)))
            	    return name 

            
class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def runServer():
    print('========== Server Start ==========')
    try:
        server = ChatingServer(('', serverPort), SocketHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('========== Server End ==========')
        server.shutdown() 
        server.server_close()
        
runServer()