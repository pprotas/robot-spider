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
        
    def grab_object(self, distance, height = -2.5):
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
        self.movement.move_servo(degree_to_position(1, 45))
        self.movement.move_servo(degree_to_position(2, 45))
        self.movement.move_servo("3,600")
        time.sleep(5)
        self.move_servo(degree_to_position(1,q1))
        self.move_servo(degree_to_position(2,90-q2))
        self.move_servo(degree_to_position(3,90-q3))
        time.sleep(5)
        self.movement.grab()
        time.sleep(2)
        self.movement.move_servo("1,600")
        self.movement.move_servo("2,50")
        self.movement.move_servo("3,800")
        
    def grab(self):
        self.move_servo(degree_to_position(4,25))
    
    def let_go(self):
        self.move_servo(degree_to_position(4,180))
    
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
                    self.move_servo(percentage_to_position(1,self.sound1))
            time.sleep(0.1)

    def move(self, move, mode="tank"):
        if (mode == "tank"):
            # instructies om spin vooruit te laten bewegen met rupsbanden
            motorA = move["a"]
            motorB = move["b"]
            print(motorA)
            print(motorB)
            self.move_servo(motorA)
            self.move_servo(motorB)

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
