import socket
import time
import cv2
import numpy as np
import base64
import pickle
import threading
import sys

HEADERSIZE = 4

server = "localhost"
port = 5556

class UDP_Client():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = server
        self.port = port+1

    def start_video(self):
        #cv2.startWindowThread()
        self.s.sendto(bytes("conn", "utf-8"), (self.ip, self.port))
        try:
            while True:
                data, client = self.s.recvfrom(2**16)
                print(data)
                if str(pickle.loads(data)) == "F":
                    break
                nparr = np.frombuffer(pickle.loads(data), np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                #encoded_frame = data[HEADERSIZE:]
                #encoded_frame = data[1]
                #frame = base64.b64decode(encoded_frame)
                cv2.imshow('Ad', frame)
                cv2.waitKey(1)

        except Exception as e:
            print(e.with_traceback())

        cv2.destroyAllWindows()
        self.s.close()





