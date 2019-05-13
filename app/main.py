from movement.movement import Movement
import time

if __name__ == '__main__':
    movement = Movement(4)
    movement.move_servo(111,111)
##    while True:
##        Temperature = movement.readNumber()
##        print("Temperature: ", Temperature)
##        Voltage = movement.readNumber()
##        print("Voltage: ", Voltage)
##        Position = movement.readNumber()
##        print("Position: ", Position*1023/255)
##        time.sleep(2)
    
