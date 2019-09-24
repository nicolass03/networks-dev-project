import socket
from _thread import *
from threading import Thread
from game import Game
from player import Player
from ball import Ball
from client_handler import ClientHandler
import pickle
import sys

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
threads = []
idCounter = 0


class threaded_client(Thread):

    def __init__(self, conn, player, gameId):
        Thread.__init__(self)
        self.gameId = gameId
        conn.send(pickle.dumps(player))

    def run(self):
        while True:
            data = pickle.loads(conn.recv(2048 * 2))
            if self.gameId in games:
                game = games[self.gameId]

                if not data:
                    break
                else:
                    if type(data) == Player:
                        if data.number == 1:
                            game.setPlayer1(data)
                        else:
                            game.setPlayer2(data)
                    else:
                        if data[0].number == 1:
                            game.setPlayer1(data[0])
                        else:
                            game.setPlayer2(data[0])
                        game.setBall(data[1])
                    print("Received: ", data)
                    print("Sending : ", game)
                    conn.send(pickle.dumps(game))
            else:
                break


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCounter += 1
    gameId = (idCounter - 1) // 2
    ball = Ball(250, 250, 20, (0, 0, 255), 500, 690)
    player = None
    if idCounter % 2 == 1:
        games[gameId] = Game(gameId)
        games[gameId].setBall(ball)
        print("New game created...")
        player = Player(0, 0, 50, 50, (0, 0, 255), 1, 500, 690)
        games[gameId].setPlayer1(player)
        p = 1
        t = threaded_client(conn,player,gameId)
        t.start()
        threads.append(t)

    else:
        games[gameId].ready = True
        player = Player(100, 100, 50, 50, (0, 255, 0), 2, 500, 690)
        games[gameId].setPlayer2(player)
        p = 2
        t = threaded_client(conn, player, gameId)
        t.start()
        threads.append(t)

for t in threads:
    t.join()
