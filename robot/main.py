from controller.controller import Controller
import sys
import os
import RPi.GPIO as GPIO
import time

if __name__ == '__main__':
    # Reset Arduino to prevent desyncing
    print("Resetting Arduino...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, 1)
    time.sleep(0.5)
    GPIO.output(26, 0)
    GPIO.cleanup()
    time.sleep(3)

    controller = Controller()
    try:
        controller.start()
    except (KeyboardInterrupt, SystemExit):  # Close the program on CTRL+C
        print("\nShutting down")
        controller.movement.move_servo("99,0")
        controller.movement.fold_legs()
        controller.movement.move_servo("1,500")
        time.sleep(3)
        controller.movement.move_servo("1,200")
        controller.movement.move_servo("2,1000")
        time.sleep(3)
        controller.movement.move_servo("3,150")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
