from movement.movement import Movement
import time

if __name__ == '__main__':
    movement = Movement('/dev/ttyUSB0')
    while True:
        movement.move_servo(254,1000)
        time.sleep(1)
        movement.move_servo(254,0)
        time.sleep(1)
    
