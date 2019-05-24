from controller.controller import Controller
import sys
import os

if __name__ == '__main__':
    controller = Controller()
    try:
        controller.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nShutting down")
        controller.movement.move_servo("99,0")

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
