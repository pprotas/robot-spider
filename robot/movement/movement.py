from i2c.i2c import I2C

class Movement:
    def __init__(self, comm):
        self.comm = comm
        print("Movement ready")
        
    def move_servo(self, servo, position):
        s = f"{servo},{position}\n"
        self.comm.writeByteBlock(s)
