import socket
import pickle


class ClientHandler:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 2000
        self.addr = (self.server, self.port)

    def getP(self):
        return self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            server_addr = pickle.loads(self.client.recv(2048 * 2))
            print(server_addr)
            self.client.close()
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(server_addr)

        except socket.error as e:
            print(e.strerror)

        return pickle.loads(self.client.recv(2048 * 2))

    def send(self, data):
        try:
            if data == "disconnect":
                self.client.send(pickle.dumps(data))
                return self.client.close()
            else:
                self.client.send(pickle.dumps(data))
                return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
