# from smbus2 import SMBus # Deze line zal crashen op Windows systemen.
import smbus2
import serial
import time

class I2C:
    def __init__(self, address):
        self.bus = smbus2.SMBus(1)
        self.address = address
        print("I2C Ready")
        
    def writeByteBlock(self, value):
        data = list(bytearray(value, 'ascii'))
        self.bus.write_i2c_block_data(self.address, 0, data)
        
    def getStatus(self):
        while True:
            Temperature = self.read()
            print("Temperature: ", Temperature)
            Voltage = self.read()
            print("Voltage: ", Voltage)
            Position = self.read()
            print("Position: ", Position*1023/255)
            time.sleep(3)
    
    
    def read(self):
        data = self.bus.read_byte(self.address)
        return data
