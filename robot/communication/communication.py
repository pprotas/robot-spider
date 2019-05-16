import websocket
import json

from threading import Thread
import time


class Communication:
    def on_message(self, message):
        self.handle_message(message)

    def on_error(self):
        print("Error")

    def on_close(self):
        print("Close")
            
    def sendPendingMessages(self):
        while True:
            messages = self.controller.messages
            if (len(messages) > 0):
                self.ws.send(messages.pop())
            time.sleep(0.05)

    def on_open(self):
        print("Connecfted.")
        Thread(target=self.sendPendingMessages).start()

    def handle_message(self, message):
        self.controller.notify(message)

    def start(self):
        while True:
            self.ws.run_forever()
            time.sleep(1)

    def __init__(self, controller):
        print("Trying to start the websocket to the server")
        self.controller = controller
        self.ws = websocket.WebSocketApp("ws://robot-spider-server.herokuapp.com/connect/robot"
                                         , on_message=self.on_message
                                         , on_error=self.on_error
                                         , on_close=self.on_close)
        self.ws.on_open = self.on_open
