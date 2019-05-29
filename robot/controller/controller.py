from communication.socket import Socket
from communication.i2c import I2C
from movement.movement import Movement, map_position
from threading import Thread
import time
import json

class Controller:

    def __init__(self):
        print("Controller started")
        self.messages = []
        # Movement center with connection to Arduino
        self.i2c = I2C(self, 4)
        self.movement = Movement(self.i2c)
        
    
    def start(self):
        # Connection to webserver
        Thread(target=Socket(self).start, daemon=True).start()
        input()
    
    def handle_message(self, message):
        j = json.loads(message)
        type = j["type"]
        # Choose appropriate movement command
        if(type == "move_motor"):
            self.movement.move(move)
        elif(type == "move_arm"):
            self.movement.move(move, "arm")
            
    
    def send(self, json):
        self.messages.append(json)