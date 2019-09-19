import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.getfqdn())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.data = self.connect()
        self.p = self.data[0]
        self.b = self.data[1]

    def getP(self):
        return self.p

    def getB(self):
        return self.b

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048*2))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)