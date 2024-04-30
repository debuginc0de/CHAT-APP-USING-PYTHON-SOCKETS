import socket
import sys
import threading

class Socket:
    def __init__(self,port):
        self.__clients = []
        self.__flag = True
        self.__serv_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__port = port
        self.__serv_sock.bind(('',self.__port))
        print("Listening...")
        self.__serv_sock.listen()

    def run(self):
        t1 = threading.Thread(target=self.__clientHandler)
        t2 = threading.Thread(target=self.__serverHandler)
        t1.start()
        t2.start()
        t2.join()
        t1.join()

    def __serverHandler(self):
        while self.__flag:
            command = input()
            l = command.lower().strip().split()
            if l[0] == 'stop' and l[1] == 'server':
                self.stopServer()
            elif l[0] == 'block' and l[1] == 'client':
                self.__clients.remove(int(l[2]))
            else:
                print("Enter valid command")



    def __clientHandler(self):
        while self.__flag:
            clnt_sock, addr = self.__serv_sock.accept()
            clnt_sock.send(b"Welcome to the server...")
            print("Client connected -","at address", addr)
            self.__clients.append(clnt_sock)
            thread = threading.Thread(target=self.__conversation,args=(clnt_sock,))
            thread.start()

    def __conversation(self,clnt_sock):
        while self.__flag:
            msg = clnt_sock.recv(1024)
            msg = msg.decode('utf-8')
            l = msg.strip().split()[-1]
            if l == 'q' or l == 'Q':
                break
            print(msg)
            if(msg != ''):
                for each in self.__clients:
                    if(each!=clnt_sock):
                        each.send(msg.encode('utf-8'))
        clnt_sock.close()

    def stopServer(self):
        for each in self.__clients:
            each.send(b'q')
            each.close()
        self.__serv_sock.close()
        self.__flag = False


if __name__ == '__main__':
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
        serv = Socket(port)
        serv.run()
        serv.stopServer()
    else:
        print("Give proper arguments...")

