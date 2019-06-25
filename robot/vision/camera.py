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
        self.delay = 0
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

                    if (len(self.requests) or (self.serverRequest and self.controller.cloudcomputer == None)):
                        img = Image.fromarray(frame.array)
                        imgByteArr = io.BytesIO()
                        img.save(imgByteArr, format='JPEG')
                        base64image = base64.b64encode(imgByteArr.getvalue())
                        
                        x = {"type": "response", "message": {"type": "image"}}
                        x["message"]["arg"] = base64image.decode('utf-8')
                        if (len(self.requests)):
                            source = self.requests.pop()
                            self.controller.cloudcomputer.messages.append(json.dumps(x))
                            
                        elif (self.serverRequest and self.controller.cloudcomputer == None):
                            if (len(self.controller.server.messages) < 3):
                                print("stuur image")
                                self.controller.server.messages.append(json.dumps(x))
                                time.sleep(self.delay)

                rawCapture.truncate(0)
                #time.sleep(self.delay)
            except:
                print("Error while creating and sending images")
            finally:
                running = False
                
    def stream(self, state, delay):
        print("change camera state")
        print(state)
        if (state == "true"):
            print("camera on")
            self.serverRequest = True
            self.delay = delay
        else:
            camara("camera off")
            self.serverRequest = False
            self.delay = delay

    def start(self):
        self.image_sender()

#start_time = time.time()
#print("tijd: ", time.time() - start_time)