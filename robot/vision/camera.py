import base64
import websocket
from threading import Thread
import time

from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera
import io

class Camera: 
    def __init__(self):
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

                    request_sourses = self.requests
                    if (len(request_sourses)):
                        img = Image.fromarray(frame.array)
                        imgByteArr = io.BytesIO()
                        img.save(imgByteArr, format='JPEG')

                        base64image = base64.b64encode(imgByteArr.getvalue())

                        source = request_sourses.pop()
                        source.messages.append("img " + base64image)

                    rawCapture.truncate(0)
                    #time.sleep(3)
            except:
                print("Error while creating and sending images")
            finally:
                running = False

    def start(self):
        self.image_sender()