import socket
import threading
from _thread import *
from game import Game
from player import Player
from ball import Ball
from udp_server import UDP_Server as userv
from client_handler import ClientHandler
import pickle
import sys

server = "localhost"
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp = userv((server, port+1))
udp_thread = threading.Thread(
                target=udp.start_video_sender,
                args=()
            )
udp_thread.start()

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("[+] Waiting for a connection, server started...")

connected = set()
games = {}
threads = []
idCounter = 0

def threaded_client(conn, player, gameId, ip, idCounter):

    conn.send(pickle.dumps(player))
    client_connected = True
    while client_connected:
        try:
            data = pickle.loads(conn.recv(2048 * 2))
            if gameId in games:
                current_game = games[gameId]
                if not data:
                    pass
                elif data == "disconnect":
                    connected.remove((ip, gameId))
                    if player.number == 1:
                        current_game.setPlayer1(None)
                    else:
                        current_game.setPlayer2(None)
                    current_game.ready = False
                    client_connected = False
                    idCounter -= 1
                    print("[-] Removed "+ip+" with gameId: "+str(gameId))
                else:
                    if type(data) == Player:
                        if data.number == 1:
                            current_game.setPlayer1(data)
                        else:
                            current_game.setPlayer2(data)

                    else:
                        if data[0].number == 1:
                            current_game.setPlayer1(data[0])
                        else:
                            current_game.setPlayer2(data[0])

                        if current_game.ball_owner == data[2]:
                            current_game.setBall(data[1])
                        elif data[3] is True:
                            current_game.ball_owner = data[2]
                            current_game.setBall(data[1])

                    #print("Received: ", data)
                    #print("Sending : ", current_game)
                    conn.send(pickle.dumps(current_game))
            else:
                pass
        except:
            client_connected = False
            print("[+] Stopped receiving data from IP "+ addr[0])


while True:
    conn, addr = s.accept()
    print("[+] Connected to:", addr)
    #udp.start_video_sender(addr)
    idCounter += 1
    gameId = (idCounter - 1) // 2
    ball = Ball(330, 220, 20, (0, 0, 255), 490, 670)
    player = None
    waiting_game = False

    for key, game in games.items():
        if not game.connected():
            waiting_game = True
            print("[+] Adding client to waiting game "+str(key)+"...")
            if type(game.p1) is None:
                player = Player(40, 225, 50, 50, (0, 0, 255), 1, 490, 670)
                games[key].setPlayer1(player)
            else:
                player = Player(640, 225, 50, 50, (0, 255, 0), 2, 490, 670)
                games[key].setPlayer2(player)
            if games[key].bothOnline():
                games[key].ready = True
                games[key].reset()
            client_thread = threading.Thread(
                target=threaded_client,
                args=(conn, player, key, addr[0], idCounter)

            )
            connected.add((addr[0], gameId))
            print("[+] Saved " + addr[0] + " with gameId: " + str(key))
            client_thread.start()
            threads.append(client_thread)
            break

    if not waiting_game:

        if idCounter % 2 == 1:

            games[gameId] = Game(gameId)
            games[gameId].setBall(ball)
            print("[+] New game created...")
            player = Player(40, 225, 50, 50, (0, 0, 255), 1, 490, 670)
            games[gameId].setPlayer1(player)
            p = 1
            client_thread = threading.Thread(
                target=threaded_client,
                args=(conn, player, gameId, addr[0], idCounter)

            )
            connected.add((addr[0], gameId))
            print("[+] Saved " + addr[0] + " with gameId: " + str(gameId))
            client_thread.start()
            threads.append(client_thread)

            # start_new_thread(threaded_client, (conn, player, gameId))

        else:
            print(type(games))
            games[gameId].ready = True
            player = Player(640, 225, 50, 50, (0, 255, 0), 2, 490, 670)
            games[gameId].setPlayer2(player)
            p = 2
            client_thread = threading.Thread(
                target=threaded_client,
                args=(conn, player, gameId, addr[0], idCounter)

            )
            connected.add((addr[0], gameId))
            print("[+] Saved " + addr[0] + " with gameId: " + str(gameId))
            client_thread.start()
            threads.append(client_thread)

            # start_new_thread(threaded_client, (conn, player, gameId))

for t in threads:
    t.join()