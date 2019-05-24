# from smbus2 import SMBus # Deze line zal crashen op Windows systemen.
import smbus2
import serial
import time
import json

class I2C:
    def __init__(self, controller, address):
        self.controller = controller
        self.bus = smbus2.SMBus(1)
        self.address = address
        print("I2C Started")
        
    def write_byte_block(self, value):
        data = list(bytearray(value, 'ascii'))
        self.bus.write_i2c_block_data(self.address, 0, data)
        time.sleep(0.05)
        
    def get_status(self):
        while True:
            self.read()
            temperature = self.read()
            voltage = self.read()
            position = self.read()
            position *= 1023/255
            json = self.controller.generate_json(["temp", "volt", "pos"],[temperature,voltage,position])
            self.controller.send(json)
            time.sleep(5)
    
    
    def read(self):
        data = self.bus.read_byte(self.address)
        return data
