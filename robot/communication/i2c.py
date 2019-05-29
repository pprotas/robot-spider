import smbus2
import time
import communication.json_gen as jg

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
    
    def read(self):
        data = self.bus.read_byte(self.address)
        return data
    
    def get_status(self):
        while True:
            self.read()
            temperature = self.read()
            servo = self.read()
            json = jg.generate_json(["highestTemperature", "servoID"],[temperature,servo])
            self.controller.send(json)
            time.sleep(5)