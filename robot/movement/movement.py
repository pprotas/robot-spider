from communication.i2c import I2C
from threading import Thread
import math
import time

class Movement:
    def __init__(self, comm):
        self.comm = comm
        self.dancing = False
        self.sound0 = 0
        self.sound1 = 0
        self.sound2 = 0
        Thread(target=self.dance, daemon=True).start()

    def move_servo(self, data):
        self.comm.write_byte_block(f"{data}\n")

    def grab_object(self, distance, height=-2.5):
        # instructies om een object op te pakken gegeven de afstand van dit object tot het arm
        print("Grabbing object in movement")

        # a, b en c zijn lengtes van de grijparm
        a = 15
        b = 10
        c = 12.5
        a2 = a*a
        b2 = b*b
        # x is de horizontale afstand tot het object
        x = distance
        # y is de hoogte van het object ten opzichte van het laagste punt van de arm
        y = height
        y2 = y*y
        # xp is de horizontale lengte naar het begin van de grijper
        xp = x - c
        xp2 = xp*xp
        # d is de afstand van het laagste punt van de grijparm tot het begin van de grijper
        d = math.sqrt(xp2 + y2)
        d2 = d*d

        # minimale en maximale waardes voor de distance
        minVal = math.sqrt(a2 + b2 - y2) + c
        maxVal = math.sqrt((a+b)*(a+b) - y2) + c

        print("minVal:", minVal)
        print("maxVal:", maxVal)

        # q1 en q2 (hoeken van servo's) worden berekend

        q2 = math.pi - math.acos((a2+b2-d2)/(2*a*b))
        q1 = math.atan(y/x) + math.acos((a2+d2-b2)/(2*a*d))
        # q1 en q2 worden omgezet naar graden
        q1 = math.degrees(q1)
        q2 = math.degrees(q2)

        # q3 wordt berekend
        q3 = q1 - q2 - 10

        # de servo's worden bewogen op basis van de berekende gegevens
        self.let_go()
        self.move_servo("1,500")
        self.move_servo("2,150")
        self.move_servo("3,850")
        time.sleep(6)
        self.move_servo("1,255")
        time.sleep(5)
        # self.move_servo("91,120")
        # self.move_servo("92,100")
        time.sleep(1)
        self.move_servo("99,0")
        self.set_speed(50)
        self.move_servo(degree_to_position(1, q1 - 10))
        self.move_servo(degree_to_position(2, 90-q2))
        self.move_servo(degree_to_position(3, 90-q3))
        time.sleep(5)
        self.grab()
        time.sleep(2)
        self.move_servo("1,600")
        self.move_servo("2,50")
        self.move_servo("3,800")
        self.set_speed(100)

    def drop_object(self):
        self.set_speed(50)
        self.move_servo(degree_to_position(1, 45))
        self.move_servo("2,50")
        self.move_servo("3,800")
        time.sleep(4)
        self.let_go()
        self.set_speed(100)

    def grab(self):
        self.move_servo(degree_to_position(4, 90))

    def let_go(self):
        self.move_servo(degree_to_position(4, 130))

    def move_to_object(self, distance):
        # instructies om de robot recht voor het object te plaatsen gegeven de afstand
        print("Moving to object")

    def dance(self):
        previous = self.sound1
        while True:
            if self.dancing:
                print(self.sound1)
                if(not(previous - 5 <= self.sound1 <= previous + 5)):
                    previous = self.sound1
                    self.move_servo(percentage_to_position(1, self.sound1))
            time.sleep(0.1)

    def move(self, move, mode="tank"):
        if (mode == "tank"):
            # instructies om spin vooruit te laten bewegen met rupsbanden
            motorA = move["a"]
            motorB = move["b"]
            print(motorB)
            print(motorA)
            self.move_servo(motorB)
            self.move_servo(motorA)            

        elif (mode == "arm"):
            moveA = move["a"]
            moveB = move["b"]

            self.move_servo(moveA)
            self.move_servo(moveB)

            valueA = int(moveA.split(",")[1])
            valueA = translate(valueA, 205, 818, 0, 180)
            valueB = int(moveB.split(",")[1])
            valueB = translate(valueB, 205, 818, 0, 180)
            print(valueA)
            print(valueB)

            valueC = 90 - (valueA - (90 - valueB)) + 10

            if(valueC >= 0 or valueC <= 180):
                moveC = degree_to_position(3, valueC)
                print(moveC)
                self.move_servo(moveC)

        elif (mode == "spider"):
            # spin beweging
            print("Moving forward as spider")

    def set_speed(self, speed):
        self.comm.write_byte_block(f"100,{speed}\n")

    def tilt_back(self):
        # Instructions to lift front of robot
        self.move_servo(degree_to_position(20, 50))
        self.move_servo(degree_to_position(30, 130))
        self.move_servo(degree_to_position(22, 0))
        self.move_servo(degree_to_position(32, 0))
        time.sleep(3)
        self.move_servo(degree_to_position(21, 160))
        self.move_servo(degree_to_position(31, 160))
        time.sleep(3)
        self.move_servo(degree_to_position(20, 130))
        self.move_servo(degree_to_position(30, 50))

    def stand_back(self):
        self.move_servo(degree_to_position(22, 50))
        self.move_servo(degree_to_position(32, 50))

    def lean_back(self):
        # self.move_servo(degree_to_position(22,0))
        # self.move_servo(degree_to_position(21,130))
        # self.move_servo(degree_to_position(20,50))
        # time.sleep(2)
        # self.move_servo(degree_to_position(21,180))
        # time.sleep(2)
        # self.move_servo(degree_to_position(32,0))
        # self.move_servo(degree_to_position(31,130))
        # self.move_servo(degree_to_position(30,130))
        # time.sleep(2)
        # self.move_servo(degree_to_position(31,180))

        self.move_servo(degree_to_position(20, 110))
        self.move_servo(degree_to_position(30, 70))
        self.move_servo(degree_to_position(21, 60))
        self.move_servo(degree_to_position(31, 60))
        self.move_servo(degree_to_position(22, 70))
        self.move_servo(degree_to_position(32, 70))
# self.move_servo(degree_to_position(21,180))
# self.move_servo(degree_to_position(31,180))

    def tilt_front(self):
        # Instructions to lift back of robot
        self.move_servo(degree_to_position(10,50))
        self.move_servo(degree_to_position(40,130))
        time.sleep(3)
        self.move_servo(degree_to_position(11,40))
        self.move_servo(degree_to_position(41,40))
        self.move_servo(degree_to_position(12,220))
        self.move_servo(degree_to_position(42,220))
        time.sleep(1)
        self.move_servo(degree_to_position(11,90))
        self.move_servo(degree_to_position(41,90))
        self.move_servo(degree_to_position(12,180))
        self.move_servo(degree_to_position(42,180))

    def support_back(self):
        self.move_servo(degree_to_position(20, 0))
        self.move_servo(degree_to_position(30, 180))
        self.move_servo(degree_to_position(22, 0))
        self.move_servo(degree_to_position(32, 0))
        time.sleep(3)
        self.move_servo(degree_to_position(21, 180))
        self.move_servo(degree_to_position(31, 180))

    def fold_legs(self):
        # Instructions to fold legs out of the way
        self.move_servo(degree_to_position(11, 0))
        self.move_servo(degree_to_position(21, 0))
        self.move_servo(degree_to_position(31, 0))
        self.move_servo(degree_to_position(41, 0))
        time.sleep(2)
        self.move_servo(degree_to_position(10, 180))
        self.move_servo(degree_to_position(20, 0))
        self.move_servo(degree_to_position(30, 180))
        self.move_servo(degree_to_position(40, 0))
        self.move_servo(degree_to_position(12, 180))
        self.move_servo(degree_to_position(22, 180))
        self.move_servo(degree_to_position(32, 180))
        self.move_servo(degree_to_position(42, 180))

    def fold_front(self):
        self.move_servo(degree_to_position(11,40))
        self.move_servo(degree_to_position(41,40))
        self.move_servo(degree_to_position(12,220))
        self.move_servo(degree_to_position(42,220))
        time.sleep(2)
        self.fold_legs()

def degree_to_position(servo, degrees):
    pos = translate(degrees, 0, 180, 205, 818)
    return f"{servo},{pos}"

def percentage_to_position(servo, percentage):
    pos = translate(percentage, 0, 100, 205, 818)
    return f"{servo},{pos}"

def translate(value, left_min, left_max, right_min, right_max):
    leftSpan = left_max - left_min
    rightSpan = right_max - right_min
    valueScaled = float(value - left_min) / float(leftSpan)
    return int(right_min + (valueScaled * rightSpan))

class SingleDance:
    
    # Contructor
    def __init__(self, comm):
        self.comm = comm

    # Start dancing
    def start(self):
        print("Singledance Start")

        time.sleep(3)
        self.move_servo(degree_to_position(1, 90))
        self.move_servo(degree_to_position(2, 90))
        self.move_servo(degree_to_position(3, 0)) 
        time.sleep(2)       

        # Move 1
        print("Move 1: leggs left to right")
        print("1: bow left to right 6 times")
        self.bow_all_leggs_left_to_right(6, 300)
        print("1: forward ride 200 140")
        self.move_direction_forward("200", "140")
        print("1: bow left to right 4 times")
        self.bow_all_leggs_left_to_right(4, 200)
        print("1: stop riding")
        self.stop()
        print("1: backward ride 200 140")
        self.move_direction_backward("200", "140")
        print("1: bow left to right 6 times")        
        self.bow_all_leggs_left_to_right(6, 200)
        print("stop")
        self.stop()
        
        # Move 2
        print("Move 2: Pirouette Left")
        self.pirouette_left(1)

        # Move 3
        print("Move 3: Rotate left with left leggs down")
        self.left_leggs_down()
        self.rotate_left_forward(8)

        # Move 4
        print("Move 4: 3 Pirouette's Right")
        self.reset_legg_upper_left()
        self.reset_legg_bottom_left()
        self.pirouette_right(3)

        # Move 5
        print("Move 5: Upper leggs bow")
        self.bow_upper_leggs(5)

        print("SingleDance Done")
    
    # Pirouette
    def pirouette_right(self, nr_of_rounds):
        time = 3.1 * nr_of_rounds
        self.reset_all_leggs()
        self.rotate_in_place_right(time)
        self.stop()
    def pirouette_left(self, nr_of_rounds):
        time = 3.1 * nr_of_rounds
        self.reset_all_leggs()
        self.rotate_in_place_left(time)
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
    
    # Bow
    def bow_upper_leggs(self, nr_of_times):
        self.set_speed(999)
        for i in range(0, nr_of_times):
            self.move_servo(degree_to_position(10, 40))
            self.move_servo(degree_to_position(40, 140))

            self.move_servo(degree_to_position(11, 0))
            self.move_servo(degree_to_position(41, 0))

            self.move_servo(degree_to_position(12, 90))
            self.move_servo(degree_to_position(42, 90))

            time.sleep(0.4)
            self.move_servo(degree_to_position(11, 90))
            self.move_servo(degree_to_position(41, 90))
            time.sleep(0.2)
        self.set_speed(100)
    def bow_all_leggs_left_to_right(self, nr_of_times, max_servo_speed):
        self.move_servo(degree_to_position(10, 120))
        self.move_servo(degree_to_position(20, 60))
        self.move_servo(degree_to_position(30, 120))
        self.move_servo(degree_to_position(40, 60))

        self.move_servo(degree_to_position(11, 0))
        self.move_servo(degree_to_position(21, 0))
        self.move_servo(degree_to_position(31, 0))
        self.move_servo(degree_to_position(42, 0))

        self.set_speed(max_servo_speed)
        for i in range(0, nr_of_times):
            self.move_servo(degree_to_position(12, 0))
            self.move_servo(degree_to_position(22, 0))
            self.move_servo(degree_to_position(32, 180))
            self.move_servo(degree_to_position(42, 180))
            time.sleep(0.5)
            
            self.move_servo(degree_to_position(12, 180))
            self.move_servo(degree_to_position(22, 180))
            self.move_servo(degree_to_position(32, 0))
            self.move_servo(degree_to_position(42, 0))
            time.sleep(0.4)
        self.set_speed(100)

    # Leggs down
    def left_leggs_down(self):
        self.reset_legg_bottom_right()
        self.reset_legg_upper_right()
        self.move_servo(degree_to_position(30, 160))
        self.move_servo(degree_to_position(40, 20))

        self.move_servo(degree_to_position(31, 90))
        self.move_servo(degree_to_position(41, 90))

        self.move_servo(degree_to_position(32, 100))
        self.move_servo(degree_to_position(42, 100))
        time.sleep(1)
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
        time.sleep(0.5)
    def reset_legg_upper_right(self):
        print("reset upper right")
        self.move_servo(degree_to_position(10, 90))
        self.move_servo(degree_to_position(11, 0))
        self.move_servo(degree_to_position(12, 30))
        time.sleep(0.5)
    def reset_legg_bottom_left(self):
        print("reset bottom left")
        self.move_servo(degree_to_position(30, 90))
        self.move_servo(degree_to_position(31, 0))
        self.move_servo(degree_to_position(32, 30))
        time.sleep(0.5)
    def reset_legg_bottom_right(self):
        print("reset bottom right")
        self.move_servo(degree_to_position(20, 90))
        self.move_servo(degree_to_position(21, 0))
        self.move_servo(degree_to_position(22, 30))
        time.sleep(0.5)

    # Stop
    def stop(self):
        self.move_servo("95,0")
        self.move_servo("96,0")   

    # Move with time
    def move_forward_with_time(self, time_forward):
        self.upper_leggs_forward()
        self.move_servo("91,200")
        self.move_servo("92,200")
        time.sleep(time_forward)
        self.stop()    
    def move_backward_with_time(self, time_backward):
        self.bottom_leggs_forward()
        self.move_servo("93,200")
        self.move_servo("94,200")
        time.sleep(time_backward)
        self.stop()
    def move_direction_forward_with_time(self, motor_a, motor_b, time_direction):
        self.upper_leggs_forward()
        self.move_servo("91," + motor_a)
        self.move_servo("92," + motor_b)
        time.sleep(time_direction)
        self.stop()
    def move_direction_backward_with_time(self, motor_a, motor_b, time_direction):
        self.bottom_leggs_forward()
        self.move_servo("93," + motor_a)
        self.move_servo("94," + motor_b)
        time.sleep(time_direction)
        self.stop()
    
    # Move no time
    def move_forward(self):
        self.upper_leggs_forward()
        self.move_servo("91,200")
        self.move_servo("92,200")
    def move_backward(self):
        self.bottom_leggs_forward()
        self.move_servo("93,200")
        self.move_servo("94,200")
    def move_direction_forward(self, motor_a, motor_b):
        self.move_servo("91," + motor_a)
        self.move_servo("92," + motor_b)
    def move_direction_backward(self, motor_a, motor_b):
        self.move_servo("93," + motor_a)
        self.move_servo("94," + motor_b)

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
        time.sleep(time_left)
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
    def set_speed(self, speed):
        self.comm.write_byte_block(f"100,{speed}\n")
