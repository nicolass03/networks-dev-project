import socket
import threading
from _thread import *
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

def threaded_client(conn, player, gameId):
    conn.send(pickle.dumps(player))

    while True:
        data = pickle.loads(conn.recv(2048 * 2))

        if gameId in games:
            game = games[gameId]

            if not data:
                pass
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
            pass



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
        client_thread = threading.Thread(
            target=threaded_client,
            args=(conn, player, gameId,)

        )
        client_thread.start()
        threads.append(client_thread)

        #start_new_thread(threaded_client, (conn, player, gameId))

    else:
        games[gameId].ready = True
        player = Player(100, 100, 50, 50, (0, 255, 0), 2, 500, 690)
        games[gameId].setPlayer2(player)
        p = 2
        client_thread = threading.Thread(
            target=threaded_client,
            args=(conn, player, gameId,)

        )
        client_thread.start()
        threads.append(client_thread)

        #start_new_thread(threaded_client, (conn, player, gameId))

for t in threads:
    t.join()