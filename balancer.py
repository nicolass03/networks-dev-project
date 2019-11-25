import os
import socket
from server import Server
import threading
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(("localhost", 2000))
    s.listen()
    print("[BALANCER] Balancer set on "+str(("localhost", 2000)))

except socket.error as e:
    print(e.strerror)

first_server = Server()
current_server = first_server
server_thread = threading.Thread(
                    target=first_server.run_server,
                    args=()
                )
server_thread.start()

while True:
    conn, addr = s.accept()
    print("[BALANCER] Connected to " + str(addr))
    if not current_server.full_capacity:
        conn.send(pickle.dumps((current_server.server, current_server.port)))
        conn.shutdown(socket.SHUT_RDWR)

    else:
        new_server = Server()
        new_server_thread = threading.Thread(
            target=new_server.run_server,
            args=()
        )
        new_server_thread.start()
        print("[BALANCER] Starting new server on " + str((new_server.server,new_server.port)))
        current_server = new_server
        conn.send(pickle.dumps((current_server.server, current_server.port)))
        conn.shutdown(socket.SHUT_RDWR)




