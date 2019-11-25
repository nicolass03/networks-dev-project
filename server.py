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
import os

class Server():
    def __init__(self):
        self.server = "localhost"
        self.port = 25555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.full_capacity = False

        while True:
            try:
                self.s.bind((self.server, self.port))
                break
            except socket.error as e:
                self.port += 1
                """"str(e)"""
        """
        udp = userv((self.server, self.port+1))
        udp_thread = threading.Thread(
                        target=udp.start_video_sender,
                        args=()
                    )
        udp_thread.start()"""
        self.s.listen()
        print("[SERVER] Waiting for a connection, server started on " + str((self.server, self.port)))

        self.connected = []
        self.games = {}
        self.threads = []
        self.idCounter = 0

    def threaded_client(self,conn, player, gameId, ip, idCounter):

        conn.send(pickle.dumps(player))
        client_connected = True
        while client_connected:
            try:
                data = pickle.loads(conn.recv(2048 * 2))
                if gameId in self.games:
                    current_game = self.games[gameId]
                    if not data:
                        pass
                    elif data == "disconnect":
                        self.connected.remove(ip)
                        if player.number == 1:
                            current_game.setPlayer1(None)
                        else:
                            current_game.setPlayer2(None)
                        current_game.ready = False
                        client_connected = False
                        idCounter -= 1
                        print("[- SERVER] Removed "+ip+" with gameId: "+str(gameId))
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
                            current_game.setBall(data[1])
                        #print("Received: ", data)
                        #print("Sending : ", current_game)
                        conn.send(pickle.dumps(current_game))
                else:
                    pass
            except:
                client_connected = False

    def run_server(self):
        while True:
            if len(self.connected) < 2:
                print("[SERVER] Clients remaining: " + str(2 - len(self.connected)))
                conn, addr = self.s.accept()
                print("[+ SERVER] Connected to:", addr)
                #udp.start_video_sender(addr)
                self.idCounter += 1
                gameId = (self.idCounter - 1) // 2
                ball = Ball(330, 220, 20, (0, 0, 255), 490, 670)
                player = None
                waiting_game = False

                for key, game in self.games.items():
                    if not game.connected():
                        waiting_game = True
                        print("[+ SERVER] Adding client to waiting game "+str(key)+"...")
                        if type(game.p1) is None:
                            player = Player(40, 225, 50, 50, (0, 0, 255), 1, 490, 670)
                            self.games[key].setPlayer1(player)
                        else:
                            player = Player(640, 225, 50, 50, (0, 255, 0), 2, 490, 670)
                            self.games[key].setPlayer2(player)
                        if self.games[key].bothOnline():
                            self.games[key].ready = True
                            self.games[key].reset()
                        client_thread = threading.Thread(
                            target=self.threaded_client,
                            args=(conn, player, key, addr[0], self.idCounter)

                        )
                        self.connected.append(addr[0])
                        print("[+ SERVER] Saved " + addr[0] + " with gameId: " + str(key))
                        client_thread.start()
                        self.threads.append(client_thread)

                if not waiting_game:

                    if self.idCounter % 2 == 1:

                        self.games[gameId] = Game(gameId)
                        self.games[gameId].setBall(ball)
                        print("[+ SERVER] New game created...")
                        player = Player(40, 225, 50, 50, (0, 0, 255), 1, 490, 670)
                        self.games[gameId].setPlayer1(player)
                        p = 1
                        client_thread = threading.Thread(
                            target=self.threaded_client,
                            args=(conn, player, gameId, addr[0], self.idCounter)

                        )
                        self.connected.append(addr[0])
                        print("[+ SERVER] Saved " + addr[0] + " with gameId: " + str(gameId))
                        client_thread.start()
                        self.threads.append(client_thread)

                        # start_new_thread(threaded_client, (conn, player, gameId))

                    else:
                        print(type(self.games))
                        self.games[gameId].ready = True
                        player = Player(640, 225, 50, 50, (0, 255, 0), 2, 490, 670)
                        self.games[gameId].setPlayer2(player)
                        p = 2
                        client_thread = threading.Thread(
                            target=self.threaded_client,
                            args=(conn, player, gameId, addr[0], self.idCounter)

                        )
                        self.connected.append(addr[0])
                        print("[+ SERVER] Saved " + addr[0] + " with gameId: " + str(gameId))
                        client_thread.start()
                        self.threads.append(client_thread)

                        # start_new_thread(threaded_client, (conn, player, gameId))
            else:
                self.full_capacity = True
        for t in threads:
            t.join()
