from movement.movement import Movement
from i2c.i2c import I2C
import serial
import time

if __name__ == '__main__':
    comm = I2C(4)
    #movement = Movement(comm)
    #movement.move_servo(111,111)
##    while True:
##        Temperature = movement.readNumber()
##        print("Temperature: ", Temperature)
##        Voltage = movement.readNumber()
##        print("Voltage: ", Voltage)
##        Position = movement.readNumber()
##        print("Position: ", Position*1023/255)
    while True:
        comm.read();
