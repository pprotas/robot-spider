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
        print("Grabbing object")

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
        self.move_servo(degree_to_position(1, q1))
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
        # self.move_servo("11,100")
        # self.move_servo("41,100")
        # time.sleep(1)
        # self.move_servo(degree_to_position(10,50))
        # self.move_servo(degree_to_position(40,130))
        # time.sleep(2)
        # self.move_servo("12,1000")
        # self.move_servo("42,1000")
        # time.sleep(3)
        # self.move_servo(degree_to_position(11,90))
        # self.move_servo(degree_to_position(41,90))
        # self.move_servo(degree_to_position(12,160))
        # self.move_servo(degree_to_position(42,160))
        # self.move_servo(degree_to_position(10,50))
        # self.move_servo(degree_to_position(40,130))
        # self.move_servo(degree_to_position(12,0))
        # self.move_servo(degree_to_position(42,0))
        # time.sleep(3)
        # self.move_servo(degree_to_position(11,160))
        # self.move_servo(degree_to_position(41,160))
        self.move_servo(degree_to_position(10, 50))
        self.move_servo(degree_to_position(40, 130))
        time.sleep(2)
        self.move_servo(degree_to_position(11, 40))
        self.move_servo(degree_to_position(41, 40))
        self.move_servo(degree_to_position(12, 100))
        self.move_servo(degree_to_position(42, 100))

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
    
    def __init__(self, comm):
        self.comm = comm

    def start(self):
        print("Singledance start")
        self.move_forward(4)
        self.pirouette_left()
        self.pirouette_right()
        self.move_backward(4)

    def pirouette_right(self):
        self.all_leggs_up()
        # time.sleep(0.5)
        # self.right_leggs_down()
        self.move_right()
        self.stop()

    def pirouette_left(self):
        # self.all_leggs_up()
        # time.sleep(0.5)
        self.left_leggs_down()
        self.move_left()
        self.stop()

    def all_leggs_up(self):
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

    def left_leggs_down(self):
        self.move_servo(degree_to_position(30, 180))
        self.move_servo(degree_to_position(40, 0))

        self.move_servo(degree_to_position(31, 90))
        self.move_servo(degree_to_position(41, 90))

        self.move_servo(degree_to_position(32, 130))
        self.move_servo(degree_to_position(42, 130))

    def right_leggs_down(self):
        self.move_servo(degree_to_position(10, 0))
        self.move_servo(degree_to_position(20, 0))

        self.move_servo(degree_to_position(11, 0))
        self.move_servo(degree_to_position(21, 90))

        self.move_servo(degree_to_position(12, 130))
        self.move_servo(degree_to_position(22, 130))

    def stop(self):
        self.move_servo("95,0")
        self.move_servo("96,0")   

    def move_forward(self, time_forward):
        self.move_servo("91,200")
        self.move_servo("92,200")
        time.sleep(time_forward)
        self.stop()    

    def move_backward(self, time_backward):
        self.move_servo("93,200")
        self.move_servo("94,200")
        time.sleep(time_backward)
        self.stop()    

    def move_left(self, time_left):
        self.move_servo("92,200")
        self.move_servo("93,200")
        time.sleep(time_left)
        self.stop()

    def move_right(self, time_right):
        self.move_servo("91,200")
        self.move_servo("94,200")
        time.sleep(time_right)
        self.stop()      
    
    #Helper functions    
    def degree_to_position(servo, degrees):
        pos = translate(degrees, 0, 180, 205, 818)
        return f"{servo},{pos}"

    def percentage_to_position(servo, percentage):
        pos = translate(percentage, 0, 100, 205, 818)
        return f"{servo},{pos}"

    def move_servo(self, data):
        self.comm.write_byte_block(f"{data}\n")
