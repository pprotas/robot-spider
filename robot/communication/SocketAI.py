import cv2
import base64
import websocket
from threading import Thread
import time


class SocketAI:
    dinko = ""
    send = True

    def on_message(self, message):
        self.handle_message(message)
        print((time.time() - self.dinko)*1000)
        self.send = True

    def on_error(self):
        print("Error")
        main()

    def on_close(self):
        print("Close")
        main()

    def image_sender(self):
        running = True

        while running:
            try:
                cam = cv2.VideoCapture(0)

                while True:
                    if 1:
                        self.dinko = time.time()
                        ret, frame = cam.read()
                        frame = cv2.resize(frame, (384, 216))
                        result, image = cv2.imencode('.jpg', frame)
                        base64image = base64.b64encode(image)
                        self.ws.send(base64image)
                        self.ws.send("<EOF>")
                        print("verzonden image")
                        self.send = False
            except:
                print("error while creating and sending images")
            finally:
                cam.release()
                running = False

    def on_open(self):
        print("Connected to server")
        Thread(target=self.image_sender).start()

    def handle_message(self, message):
        print(message)

    def start(self):
        while True:
            self.ws.run_forever()
            time.sleep(1)

    def __init__(self, controller):
        print("Trying to connect to the server")
        self.controller = controller
        self.ws = websocket.WebSocketApp("ws://141.252.29.41:5000/"
                                         , on_message=self.on_message
                                         , on_error=self.on_error
                                         , on_close=self.on_close)
        self.ws.on_open = self.on_open