from movement.movement import Movement
import time

if __name__ == '__main__':
<<<<<<< HEAD
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
    
=======
    movement = Movement(0x4)
    movement.move_servo(1, 0)
>>>>>>> 747e1c33e84229024897a84830139cd8108bb0bc
