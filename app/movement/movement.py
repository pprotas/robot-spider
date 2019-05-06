import serial

#port = '/dev/ttyUSB0' # Je USB poort voor de Arduino
class Movement:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600)

    def move_servo(self, servo, position):
        s = f"{servo},{position}"
        self.ser.write(s.encode())