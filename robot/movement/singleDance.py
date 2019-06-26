from communication.i2c import I2C
from threading import Thread
import math
import time

class SingleDance:
    
    # Contructor
    def __init__(self, comm):
        self.comm = comm

    # Start dancing
    def start(self):
        print("Singledance Start")
        # self.pirouette_left()
        self.move_forward(10)
        print("SingleDance Done")
    
    # Pirouette
    def pirouette_right(self):
        self.right_leggs_down()
        self.rotate_in_place_right(3)
        self.stop()
    def pirouette_left(self):
        self.left_leggs_down()
        self.rotate_in_place_left(10)
        self.stop()

    # All leggs
    def reset_all_leggs(self):
        self.move_servo(degree_to_position(10, 90))
        self.move_servo(degree_to_position(20, 90))
        self.move_servo(degree_to_position(30, 90))
        self.move_servo(degree_to_position(40, 90))

        self.move_servo(degree_to_position(11, 0))
        self.move_servo(degree_to_position(21, 0))
        self.move_servo(degree_to_position(31, 0))
        self.move_servo(degree_to_position(41, 0))

        self.move_servo(degree_to_position(12, 30))
        self.move_servo(degree_to_position(22, 30))
        self.move_servo(degree_to_position(32, 30))
        self.move_servo(degree_to_position(42, 30))

    # Leggs down
    def left_leggs_down(self):
        self.reset_legg_bottom_right()
        self.reset_legg_upper_right()
        self.move_servo(degree_to_position(30, 160))
        self.move_servo(degree_to_position(40, 20))

        self.move_servo(degree_to_position(31, 90))
        self.move_servo(degree_to_position(41, 90))

        self.move_servo(degree_to_position(32, 130))
        self.move_servo(degree_to_position(42, 130))
    def right_leggs_down(self):
        self.reset_legg_bottom_left()
        self.reset_legg_upper_left()
        self.move_servo(degree_to_position(10, 0))
        self.move_servo(degree_to_position(20, 0))

        self.move_servo(degree_to_position(11, 0))
        self.move_servo(degree_to_position(21, 90))

        self.move_servo(degree_to_position(12, 100))
        self.move_servo(degree_to_position(22, 100))

    # Leggs forward
    def upper_leggs_forward(self):
        self.reset_legg_upper_left()
        self.reset_legg_upper_right()

        self.move_servo(degree_to_position(10, 140))
        self.move_servo(degree_to_position(40, 30))

        self.move_servo(degree_to_position(11, 90))
        self.move_servo(degree_to_position(41, 90))

        self.move_servo(degree_to_position(12, 90))
        self.move_servo(degree_to_position(42, 90))
    def bottom_leggs_forward(self):
        self.reset_legg_bottom_left()
        self.reset_legg_bottom_right()
        self.move_servo(degree_to_position(20, 140))
        self.move_servo(degree_to_position(30, 30))

        self.move_servo(degree_to_position(21, 90))
        self.move_servo(degree_to_position(31, 90))

        self.move_servo(degree_to_position(22, 90))
        self.move_servo(degree_to_position(32, 90))

    # Reset to leggs middle position
    def reset_legg_upper_left(self):
        print("reset upper left")
        self.move_servo(degree_to_position(40, 90))
        self.move_servo(degree_to_position(41, 0))
        self.move_servo(degree_to_position(42, 30))
    def reset_legg_upper_right(self):
        print("reset upper right")
        self.move_servo(degree_to_position(10, 90))
        self.move_servo(degree_to_position(11, 0))
        self.move_servo(degree_to_position(12, 30))
    def reset_legg_bottom_left(self):
        print("reset bottom left")
        self.move_servo(degree_to_position(30, 90))
        self.move_servo(degree_to_position(31, 0))
        self.move_servo(degree_to_position(32, 30))
    def reset_legg_bottom_right(self):
        print("reset bottom right")
        self.move_servo(degree_to_position(20, 90))
        self.move_servo(degree_to_position(21, 0))
        self.move_servo(degree_to_position(22, 30))

    # Stop
    def stop(self):
        self.move_servo("95,0")
        self.move_servo("96,0")   

    # Move
    def move_forward(self, time_forward):
        self.upper_leggs_forward()
        self.move_servo("91,200")
        self.move_servo("92,200")
        time.sleep(10)
        self.stop()    
    def move_backward(self, time_backward):
        self.bottom_leggs_forward()
        self.move_servo("93,200")
        self.move_servo("94,200")
        time.sleep(time_backward)
        self.stop()
    def move_direction_forward(self, motor_a, motor_b, time_direction):
        self.upper_leggs_forward()
        self.move_servo("91," + motor_a)
        self.move_servo("92," + motor_b)
        time.sleep(time_direction)
        self.stop()
    def move_direction_backward(self, motor_a, motor_b, time_direction):
        self.bottom_leggs_forward()
        self.move_servo("93," + motor_a)
        self.move_servo("94," + motor_b)
        time.sleep(time_direction)
        self.stop()

    # Rotate right
    def rotate_right_forward(self, time_right_motor):
        self.move_servo("91,200")
        time.sleep(time_right_motor)
        self.stop()
    def rotate_right_backward(self, time_right_motor):
        self.move_servo("93,200")
        time.sleep(time_right_motor)
        self.stop()

    # Rotate left
    def rotate_left_forward(self, time_left_motor):
        self.move_servo("92,200")
        time.sleep(time_left_motor)
        self.stop()
    def rotate_left_backward(self, time_left_motor):
        self.move_servo("94,200")
        time.sleep(time_left_motor)
        self.stop()

    # Rotate in place, one round takes
    def rotate_in_place_left(self, time_left):
        self.move_servo("92,200")
        self.move_servo("93,200")
        time.sleep(10)
        self.stop()
    def rotate_in_place_right(self, time_right):
        self.move_servo("91,200")
        self.move_servo("94,200")
        time.sleep(time_right)
        self.stop()      

    # Helper functions    
    def degree_to_position(servo, degrees):
        pos = translate(degrees, 0, 180, 205, 818)
        return f"{servo},{pos}"
    def percentage_to_position(servo, percentage):
        pos = translate(percentage, 0, 100, 205, 818)
        return f"{servo},{pos}"
    def move_servo(self, data):
        self.comm.write_byte_block(f"{data}\n")
