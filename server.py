import socket
from _thread import *
from game import Game
from player import Player
import pickle
import sys

server = socket.gethostbyname(socket.getfqdn())
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
idCounter = 0


def threaded_client(conn, player, gameId):
    global idCount
    conn.send(pickle.dumps(player))

    response = ""

    while True:
        data = pickle.loads(conn.recv(2048 * 2))
        if gameId in games:
            game = games[gameId]

            if not data:
                break
            else:
                if data.number == 1:
                    game.p1 = data
                else:
                    game.p2 = data

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
    player = None
    if idCounter % 2 == 1:
        games[gameId] = Game(gameId)
        print("New game created...")
        player = Player(0, 0, 50, 50, (0, 0, 255), 1)
        games[gameId].p1 = player
        p = 1
    else:
        games[gameId].ready = True
        player = Player(100, 100, 50, 50, (0, 255, 0), 2)
        games[gameId].p2 = player
        p = 2

    start_new_thread(threaded_client, (conn, player, gameId))
