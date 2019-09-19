import socket
from _thread import *
from game import Game
from player import Player
from ball import Ball
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


def threaded_client(conn, player, ball, gameId):
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
                if data[0].number == 1:
                    game.p1 = data[0]
                else:
                    game.p2 = data[0]
                game.ball = data[1]

                print("Received: ", data)
                print("Sending : ", game)
                conn.send(pickle.dumps(game))
        else:
            break


ball = None

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    idCounter += 1
    gameId = (idCounter - 1) // 2
    player = None

    if idCounter % 2 == 1:
        games[gameId] = Game(gameId)
        print("New game created...")
        player = Player(225, 0, 50, 50, (0, 0, 255), 1, 500, 500)
        ball = Ball(250, 250, 20, (0, 0, 255), 500, 500)
        games[gameId].p1 = player
        games[gameId].ball = ball
        p = 1
    else:
        games[gameId].ready = True
        player = Player(225, 450, 50, 50, (0, 255, 0), 2, 500, 500)
        games[gameId].p2 = player
        p = 2

    start_new_thread(threaded_client, (conn, player, ball, gameId))
