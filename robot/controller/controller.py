from communication.communication import Communication
from movement.movement import Movement, map_position
from i2c.i2c import I2C
from threading import Thread
import time
import json
import random

class Controller:

    def __init__(self):
        print("Controller started")
        self.messages = []
        self.i2c = I2C(self, 4)
        self.movement = Movement(self.i2c)
        #self.movement.move_servo(map_position(254,90))
        #self.movement.grab_object(16)
        
    
    def start(self):
        Thread(target=Communication(self).start).start()
        Thread(target=self.i2c.get_status).start()
        while True:
            self.movement.grab_object(16)
            time.sleep(2)
            self.movement.move_servo(map_position(254,90))
            time.sleep(2)
            input()
    
    def notify(self, message):
        j = json.loads(message)
        type = j["type"]
        if(type == "move"):
            move = j["message"]["move"]
            self.movement.move(move)
            
    
    def send(self, json):
        self.messages.append(json)


    def generate_json(self, keys, values):
        x = {
                "type" : "status",
                "message" : {
                    "status" : "online"
                    }
            }
        
        for i in range(len(keys)):
            x["message"][keys[i]] = values[i]
            
        return json.dumps(x)