import base64
import websocket
from threading import Thread
import time

from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera
import io


class AI_Socket:
    dinko = ""
    send = True

    def on_message(self, message):
        self.controller.handle_message(message)

    def on_error(self):
        print("Error")
        self.start()

    def on_close(self):
        print("No connection to AI server.")
        self.start()

    def image_sender(self):
        running = True

        while running:
            if self.send:
                try:
                    camera = PiCamera()
                    camera.resolution = (384, 216)
                    rawCapture = PiRGBArray(camera, size=(384, 216))

                    for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
                        rawCapture.truncate()
                        rawCapture.seek(0)
                        self.dinko = time.time()
                        img = Image.fromarray(frame.array)
                        imgByteArr = io.BytesIO()
                        img.save(imgByteArr, format='JPEG')

                        base64image = base64.b64encode(imgByteArr.getvalue())
                        self.ws.send("img ")
                        self.ws.send(base64image)
                        self.ws.send("<EOF>")
                        self.send = False
                        rawCapture.truncate(0)
                except:
                    print("Error while creating and sending images")
                finally:
                    running = False

    def on_open(self):
        print("Connected to AI server.")
        time.sleep(3)
        self.ws.send("mode block")
        self.ws.send("<EOF>")
        time.sleep(3)
        Thread(target=self.image_sender).start()

    def handle_message(self, message):
        if message["type"] == "request":
            self.handle_request(message)

    def handle_request(self, message):
        if message["type"]["message"]["type"] == "image":
            self.send = True

    def start(self):
        while True:
            self.ws.run_forever()
            time.sleep(1)

    def __init__(self, controller):
        print("Trying to connect to the AI server")
        self.ws = websocket.WebSocketApp(
            "ws://141.252.29.41:5000/", on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.controller = controller
