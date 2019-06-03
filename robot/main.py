from controller.controller import Controller
import sys
import os

if __name__ == '__main__':
    controller = Controller()
    try:
        controller.start()
    except (KeyboardInterrupt, SystemExit): # Close the program on CTRL+C
        print("\nShutting down")
        controller.movement.move_servo("99,0")
        controller.movement.move_servo("254,500")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)