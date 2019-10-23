import socket
import cv2
import pickle
import time
import threading
from _thread import *
import base64

HEADERSIZE = 4

class UDP_Server():
    def __init__(self, addr):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = addr[0]
        self.port = addr[1]
        try:
            self.s.bind((self.ip, self.port))
            print("[+] Server started on " + self.ip)
        except socket.error as e:
            print("[-] Couldn't start server on " + self.ip)
        self.connected_clients = set()
        self.video_frames = []
        self.cap = cv2.VideoCapture('video.mp4')
        self.init_video()


    def init_video(self):
        print("[+] Server is loading the video, please wait...")
        # Read until video is completed
        for i in range(0, 2048):
            if not self.cap.isOpened():
                print("Error loading the file.")
                break
            else:
                ret, frame = self.cap.read()
                if ret:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                    # encoded_frame = base64.b64encode(buffer)
                    # data = f"{i:04d}"+str(encoded_frame)
                    data = cv2.imencode('.jpg', frame, encode_param)[1].tostring()
                    self.video_frames.append(data)

        # When everything done, release
        # the video capture object
        self.cap.release()
        print("[+] Video is loaded, server ready to stream...")


    def client_thread(self, address):
        try:
            for x in self.video_frames:
                self.s.sendto(pickle.dumps(x), address)
                time.sleep(0.016)
            self.s.sendto(pickle.dumps("F"), address)
            self.connected_clients.remove(address)
        except Exception as e:
            print(e)


    """
    def client_thread(address):
        try:
            for i in range(0,2048):
                if not cap.isOpened():
                    print("Error loading the file.")
                    break
                else:
                    ret, frame = cap.read()
                    if ret:
                        ret, buffer = cv2.imencode('.jpg', frame)
                        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                        #encoded_frame = base64.b64encode(buffer)
                        #data = f"{i:04d}"+str(encoded_frame)
                        data = cv2.imencode('.jpg', frame, encode_param)[1].tostring()
                        s.sendto(pickle.dumps(data), address)
        except Exception as e:
            print(e)
    
    """


    def start_video_sender(self):
        print("[+] Into sender...")
        while True:
            data, client = self.s.recvfrom(2 ** 16)
            if not client in self.connected_clients:
                print("[+] Now streaming to " + str(client[0]))
                self.connected_clients.add(client)
                t = threading.Thread(
                    target=self.client_thread,
                    args=(client,)

                )
                t.start()