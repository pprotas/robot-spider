import websocket
import json

from threading import Thread
import time


class Socket:
    def on_message(self, message):
        self.controller.handle_message(message)

    def on_error(self):
        print("Error")

    def on_close_main(self):
        print("No connection to main server.")
        time.sleep(3)
        
    def on_close_ai(self):
        print("No connection to AI server.")
        time.sleep(3)
            
    def sendPendingMessages(self):
        while True:
            messages = self.controller.messages
            if (len(messages)):
                self.ws.send(messages.pop())
            time.sleep(3)

    def on_open(self):
        print("Connected to server.")
        Thread(target=self.sendPendingMessages, daemon=True).start()


    def start(self):
        while True:
            self.ws.run_forever()
            time.sleep(1)

    def __init__(self, controller):
        print("Trying to start the websocket to the server")
        self.controller = controller
        self.ws = websocket.WebSocketApp("wss://robot-spider-server.herokuapp.com/connect/robot",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close_main,
                                         on_open=self.on_open)
        self.ws_ai = websocket.WebSocketApp("wss://robot-spider-server.herokuapp.com/connect/robot",
                                            on_message=self.on_message,
                                            on_error=self.on_error,
                                            on_close=self.on_close_ai,
                                            on_open=self.on_open)