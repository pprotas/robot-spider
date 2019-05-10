from movement.movement import Movement
import time

if __name__ == '__main__':
    movement = Movement(0x4)
    movement.move_servo(1, 0)
