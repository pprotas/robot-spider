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
        print("I2C Readyyyyy")
        
    def writeByteBlock(self, value):
        data = list(bytearray(value, 'ascii'))
        self.bus.write_i2c_block_data(self.address, 0, data)
        time.sleep(0.05)
        
    def getStatus(self):
        while True:
            self.read()
            Temperature = self.read()
            print("Temperature: ", Temperature)
            Voltage = self.read()
            print("Voltage: ", Voltage)
            Position = self.read()
            Position *= 1023/255
            print("Position: ", Position)
            json = self.generateJSON(["temp", "volt", "pos"],[Temperature,Voltage,Position])
            print(json)
            self.controller.send(json)
            time.sleep(5)
        
    def generateJSON(self, keys, values):
        x = {
                "type": "status",
                "message": {
                    "status": "online"
                }
            }
        
        for i in range(len(keys)):
            x["message"][keys[i]] = values[i]

        return json.dumps(x)
    
    
    def read(self):
        data = self.bus.read_byte(self.address)
        return data
