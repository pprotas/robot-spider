import websocket
import json

try:
    import thread
except ImportError:
    import _thread as thread
import time


class Communication:
    def on_message(self, message):
        self.handle_message(message)

    def on_error(self):
        print("Error")

    def on_close(self):
        print("Close")

    def status(self):
        while True:
            x = {
                "type": "status",
                "message": {
                    "temp" : 
                }
            }

            y = json.dumps(x)
            self.ws.send(y)

            time.sleep(5)
            
    def send(self, message):
        thread.start_new(self.ws.send(message))

    def on_open(self):
        print("Connected.")
        thread.start_new(self.status)

    def handle_message(self, message):
        self.controller.notify(message)

    def start(self):
        while True:
            self.ws.run_forever()
            time.sleep(1)

    def __init__(self, controller):
        print("Trying to start the websocket to the server")
        self.controller = controller
        self.ws = websocket.WebSocketApp("ws://192.168.43.36:5000/connect/robot"
                                         , on_message=self.on_message
                                         , on_error=self.on_error
                                         , on_close=self.on_close)
        self.ws.on_open = self.on_open
