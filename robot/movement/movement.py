import smbus2
import time


class Movement:
    def __init__(self, address):
        self.bus = smbus2.SMBus(1)
        self.address = address

    def writeByte(self, value):
        for c in str(value):
            self.bus.write_byte(self.address, ord(c))
            time.sleep(0.1)
        return -1

    def readNumber(self):
        number = self.bus.read_byte(address)
        return number

    def move_servo(self, servo, position):
        s = f"{servo},{position}\n"
        self.writeByte(s)
