from communication.i2c import I2C
from threading import Thread
import math
import time

class Movement:
    def __init__(self, comm):
        self.comm = comm
        self.dancing = False
        self.sound = 0
        Thread(target=self.dance, daemon=True).start()
        
    def move_servo(self, data):
        self.comm.write_byte_block(f"{data}\n")
        
    def grab_object(self, distance):
        # instructies om een object op te pakken gegeven de afstand van dit object tot het arm
        print("Grabbing object")
        a = 11
        b = 5.3
        c = 4
        a2 = a*a
        b2 = b*b
        distance2 = distance*distance
        y = 2
        y2 = y*y
        x = math.sqrt(distance2 - y2)
        xp = x - c
        xp2 = xp*xp
        d = math.sqrt(xp2 + y2)
        d2 = d*d
        
        minVal = math.sqrt(math.pow(math.sqrt(a2 + b2 - y2) + c, 2) + y2)
        #maxVal = a + b + c
        maxVal = math.sqrt(math.pow(math.sqrt((a+b)*(a+b) - y2) + c, 2) + y2)
        
        print("minVal:", minVal)
        print("maxVal:", maxVal)
        
        q2 = math.pi - math.acos((a2+b2-d2)/(2*a*b))
        q1 = math.atan(y/x) + math.acos((a2+d2-b2)/(2*a*d))
        q1 = math.degrees(q1)
        q2 = math.degrees(q2)
        
        q3 = q1 - q2
        
        self.move_servo(degree_to_position(1,q1))
        self.move_servo(degree_to_position(2,90-q2))
        self.move_servo(degree_to_position(3,90-q3))
        
    def move_to_object(self, distance):
        # instructies om de robot recht voor het object te plaatsen gegeven de afstand
        print("Moving to object")
        
    def dance(self):
        previous = self.sound
        while True:   
            if self.dancing:
                print(self.sound)
                if(not(previous - 5 <= self.sound <= previous + 5)):
                    previous = self.sound
                    self.move_servo(percentage_to_position(1,self.sound))
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
            valueC = 90 - (valueA - (90 - valueB))
            
            if(valueC >= 0 or valueC <= 180):
                moveC = degree_to_position(3, valueC)
                print(moveC)
                self.move_servo(moveC)
            
        elif (mode == "spider"):
            # spin beweging
            print("Moving forward as spider")
            
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