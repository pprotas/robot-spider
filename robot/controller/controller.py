from communication.communication import Communication
from movement.movement import Movement
from i2c.i2c import I2C
from threading import Thread
from state.controlState.classes.stairState import StairState
import time
import json

class Controller:

    def __init__(self):
        print("controller startfed")
        self.messages = []
        self.i2c = I2C(self, 4)
        self.movement = Movement(self.i2c)
        
        #self.movement.move_servo(95,0)
        #self.movement.move_servo(96,0)
        #self.movement.move_servo("1,500")
        Thread(target=Communication(self).start).start()
        Thread(target=StairState().start).start()
        Thread(target=self.i2c.getStatus).start()
        input()

    def notify(self, message):
        print(message)
        jsonM = json.loads(message)
        move = jsonM["message"]["move"]
        print(move)
        self.movement.move_servo(move)
    
    def send(self, json):
        self.messages.append(json)

    def move(self):
        movement = Movement(0x4)
        movement.move_servo(1, 0)

