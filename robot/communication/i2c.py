import smbus2
import time
import communication.json_gen as jg
from threading import Thread

class I2C:
    def __init__(self, controller, address):
        self.controller = controller
        self.bus = smbus2.SMBus(1)
        self.address = address
        self.json = ""
        print("I2C Started")
        
    def write_byte_block(self, value):
        data = list(bytearray(value, 'ascii'))
        self.bus.write_i2c_block_data(self.address, 0, data)
        time.sleep(0.05)
    
    def read(self):
        data = self.bus.read_byte(self.address)
        return data
    
    def get_status(self):
        Thread(target=self.send_status, daemon=True).start()
        while True:
            temperature = self.read()
            servo = self.read()
            sound = self.read()
            self.controller.movement.sound = sound
            self.json = jg.generate_json(["temp", "servoID", "sound"],[temperature,servo,sound])
            
            
    def send_status(self):
        while True:
            self.controller.send(self.json)
            time.sleep(10)
