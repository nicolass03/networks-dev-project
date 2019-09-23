import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.getfqdn())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.start_info = self.connect()
        self.b = self.start_info.ball_pos

    def getStartInfo(self):
        return self.start_info

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


class StartData:
    def __init__(self, player_pos1, player_pos2, number, ball_pos):
        self.player_pos1 = player_pos1
        self.player_pos2 = player_pos2
        self.number = number
        self.ball_pos = ball_pos


class GameData:
    def __init__(self, player_pos, number, ball_pos, ball_owner, new_owner):
        self.player_pos = player_pos
        self.number = number
        self.ball_pos = ball_pos
        self.ball_owner = ball_owner
        self.new_owner = new_owner

