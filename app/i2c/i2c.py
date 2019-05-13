from smbus2 import SMBus # Deze line zal crashen op Windows systemen.

class I2C:
    def __init__(self, address):
        self.bus = SMBus(1)
        self.address = address
        print("I2C Ready")
        
    def writeByteBlock(self, value):
        data = list(bytearray(value, 'ascii'))
        print(data)
        self.bus.write_i2c_block_data(self.address, 0, data)
        
    def readNumber(self):
        number = self.bus.read_byte(self.address)
        return number
    
    def read(self):
        data = self.bus.read_i2c_block_data(self.address, 0)
        return data