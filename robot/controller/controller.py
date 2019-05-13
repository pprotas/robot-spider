from robot.communication.communication import Communication
from robot.movement.movement import Movement
from threading import Thread
from robot.state.controlState.classes.stairState import StairState


class Controller:

    def __init__(self):
        print("controller started")
        Thread(target=Communication(self).start).start()
        Thread(target=StairState().start).start()
        input()

    def notify(self, message):
        print(message)

    def move(self):
        movement = Movement(0x4)
        movement.move_servo(1, 0)

