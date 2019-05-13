import smbus2  # Deze line zal crashen op Windows systemen.
import time


class Movement:
    def __init__(self, address):
        self.bus = smbus.SMBus(1)
        self.address = address

    def writeByte(self, value):
        data = list(bytearray(value, 'ascii'))
        print(data)
        self.bus.write_i2c_block_data(self.address, 0, data)
        return -1
<<<<<<< HEAD
        
    def readNumber(self):
        number = self.bus.read_byte(self.address)
=======

    def readNumber():
        number = self.bus.read_byte(address)
>>>>>>> 747e1c33e84229024897a84830139cd8108bb0bc
        return number

    def move_servo(self, servo, position):
        s = f"{servo},{position}\n"
        self.writeByte(s)
