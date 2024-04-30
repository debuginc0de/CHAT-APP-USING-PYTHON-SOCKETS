import socket
import sys
import threading


class Client:
    def __init__(self, name, host, port):
        self.__socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__port = port
        self.__host = host
        self.__flag = True
        self.__name = name

    def connect(self):
        self.__socket.connect((self.__host,self.__port))
        msg = self.__socket.recv(1024)
        print(msg.decode('utf-8'))

    def __reader(self):
        while self.__flag:
            msg = self.__socket.recv(1024)
            if msg == 'q' or msg == 'Q':
                self.__socket.close()
                print("server is closed.")
                self.__flag = False
                break
            print(msg.decode('utf-8'))

    def __writer(self):
        while self.__flag:
            msg = input()
            if msg == 'q' or msg == 'Q':
                self.__socket.close()
                self.__flag = False
                break
            msg = '@'+self.__name+' : '+msg
            self.__socket.send(msg.encode('utf-8'))

    def run(self):
        reader_thread = threading.Thread(target=self.__reader)
        writer_thread = threading.Thread(target=self.__writer)

        reader_thread.start()
        writer_thread.start()

        reader_thread.join()
        writer_thread.join()


if __name__ == '__main__':
    if len(sys.argv) == 4:
        name = sys.argv[1]
        host = sys.argv[2]
        port = int(sys.argv[3])
        client = Client(name,host,port)
        client.connect()
        client.run()
    else:
        print("Give proper arguments..")

