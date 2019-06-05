from communication.socket import Socket
<<<<<<< HEAD
from communication.i2c import I2C
from movement.movement import Movement
=======
from communication.SocketAI import SocketAI
#from communication.i2c import I2C
#from movement.movement import Movement, map_position
>>>>>>> 4f0bcda5b9fb9e0c4ddaa89db4da3ceffbd4d74d
from threading import Thread
import time
import json

class Controller:

    def __init__(self):
        print("Controller started")
        self.messages = []
        # Movement center with connection to Arduino
        #self.i2c = I2C(self, 4)
        #self.movement = Movement(self.i2c)
        
    
    def start(self):
        # Connection to webserver
        Thread(target=Socket(self).start, daemon=True).start()
        Thread(target=SocketAI(self).start, daemon=True).start()
        # Status checker
        Thread(target=self.i2c.get_status, daemon=True).start()
        self.movement.move_servo("20,100")
        input()
        
    def handle_message(self, message):
        j = json.loads(message)
        print(message)
        type = j["type"]
        move = j["message"]["move"]
        # Choose appropriate movement command
<<<<<<< HEAD
        if(type == "move_motor"):
            self.movement.move(move)
        elif(type == "move_arm"):
            self.movement.move(move, "arm")
        elif(type == "toggle_dance"):
            self.movement.dancing = move["value"]
=======
        #if(type == "move_motor"):
            #self.movement.move(move)
        #elif(type == "move_arm"):
            #self.movement.move(move, "arm")
>>>>>>> 4f0bcda5b9fb9e0c4ddaa89db4da3ceffbd4d74d
            
    
    def send(self, json):
        self.messages.append(json)