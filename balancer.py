import os
import socket
from server import Server
import threading
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servers = []
try:
    s.bind(("localhost", 2000))
    s.listen()
    print("[BALANCER] Balancer set on "+str(("localhost", 2000)))

except socket.error as e:
    print(e.strerror)

first_server = Server(0)
current_server = first_server
server_thread = threading.Thread(
                    target=first_server.run_server,
                    args=()
                )
server_thread.start()
servers.append(first_server)

def check_servers():
    while True:
        for server in servers:
            hostname = str(server.server)+":"+str(server.port)
            response = os.system("ping -c 1 " + hostname)
            if response == 0:
                pass
            else:
                new_server = Server(1)
                with open(str(server.server)+"_"+str(server.port)+".bck", 'rb') as backup:
                    server_data = pickle.load(backup)
                    new_server.connected = server_data[0]
                    new_server.games = server_data[1]
                    new_server.idCounter = server_data[2]
                    new_server.full_capacity = server_data[3]
                new_server_thread = threading.Thread(
                    target=new_server.run_server,
                    args=()
                )
                new_server_thread.start()
                servers.append(new_server)
                print("[BALANCER] Starting new server on " + str((new_server.server, new_server.port)))

check_thread = threading.Thread(
                    target=check_servers,
                    args=()
                )

while True:
    conn, addr = s.accept()
    print("[BALANCER] Connected to " + str(addr))
    if not current_server.full_capacity:
        conn.send(pickle.dumps((current_server.server, current_server.port)))
        conn.shutdown(socket.SHUT_RDWR)

    else:
        new_server = Server(0)
        new_server_thread = threading.Thread(
            target=new_server.run_server,
            args=()
        )
        new_server_thread.start()
        servers.append(new_server)
        print("[BALANCER] Starting new server on " + str((new_server.server,new_server.port)))
        current_server = new_server
        conn.send(pickle.dumps((current_server.server, current_server.port)))
        conn.shutdown(socket.SHUT_RDWR)




