import base64
import websocket
from threading import Thread
import time

from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera
import io
import json

class Camera: 
    def __init__(self, controller):
        self.controller = controller
        self.serverRequest = False
        self.requests = []

    def image_sender(self):
        running = True

        while running:
            try:
                camera = PiCamera()
                camera.resolution = (384, 216)
                rawCapture = PiRGBArray(camera, size=(384, 216))

                for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
                    rawCapture.truncate()
                    rawCapture.seek(0)

                    #request_sourses = self.requests
                    #print("Send")
                    if (self.serverRequest):
                        print("if")
                        img = Image.fromarray(frame.array)
                        print("img")
                        imgByteArr = io.BytesIO()
                        print("imgArray")
                        img.save(imgByteArr, format='JPEG')
                        print("base")
                        base64image = base64.b64encode(imgByteArr.getvalue())
                        print("base64")
                        
                        source = self.requests.pop()
                        x = {"type": "response", "message": {"type": "image"}}
                        x["message"]["arg"] = base64image.decode('utf-8')
                        print(json.dumps(x))
                        self.controller.server.messages.append(json.dumps(x))

                    rawCapture.truncate(0)
                    time.sleep(0.1)
            except:
                print("Error while creating and sending images")
            finally:
                running = False

    def start(self):
        self.image_sender()