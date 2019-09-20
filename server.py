import socket
from _thread import *
from game import Game
from player import Player
from ball import Ball
import pickle
import sys
from network import StartData, GameData

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


def threaded_client(conn, startData, gameId):
    global idCount
    conn.send(pickle.dumps(startData))

    response = ""

    while True:
        data = pickle.loads(conn.recv(2048 * 2))
        if gameId in games:
            game = games[gameId]

            if not data:
                break
            else:
                if data.number == 1:
                    game.p1 = data.player_pos
                    game.ball = data.ball
                else:
                    game.p2 = data.player_pos

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
    player_pos1 = (225, 0)
    player_pos2 = (225, 450)

    if idCounter % 2 == 1:
        games[gameId] = Game(gameId)
        print("New game created...")
        ball = Ball(250, 250, 20, (0, 0, 255), 500, 500)
        games[gameId].p1 = player_pos1
        games[gameId].ball = ball
        p = 1
        start_new_thread(threaded_client, (conn, StartData(player_pos1, player_pos2, 1, ball), gameId))
    else:
        games[gameId].ready = True
        games[gameId].p2 = player_pos2
        p = 2
        start_new_thread(threaded_client, (conn, StartData(player_pos2, player_pos1, 2, ball), gameId))

