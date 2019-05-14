from communication.communication import Communication
from movement.movement import Movement
from i2c.i2c import I2C
from threading import Thread
from state.controlState.classes.stairState import StairState


class Controller:

    def __init__(self):
        print("controller startfed")
        self.messages = []
        i2c = I2C(self, 4)
        Thread(target=Communication(self).start).start()
        Thread(target=StairState().start).start()
        Thread(target=i2c.getStatus).start()
        input()

    def notify(self, message):
        print(message)
    
    def send(self, json):
        self.messages.append(json)

    def move(self):
        movement = Movement(0x4)
        movement.move_servo(1, 0)

