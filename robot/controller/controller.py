from communication.socket import Socket
from communication.ai_socket import AI_Socket
from communication.i2c import I2C
from movement.movement import Movement, degree_to_position
from threading import Thread
import time
import json


class Controller:

    def __init__(self):
        print("Program started")
        self.messages = []
        # Movement center with connection to Arduino
        self.i2c = I2C(self, 4)
        self.movement = Movement(self.i2c)
        
    def start(self):
        # Connection to webserver
        Thread(target=Socket(self).start, daemon=True).start()
        Thread(target=AI_Socket(self).start, daemon=True).start()
        # Status checker
        Thread(target=self.i2c.get_status, daemon=True).start()
        self.movement.move_servo("2,150")
        self.movement.move_servo("3,600")
        time.sleep(5)
        self.movement.grab_object(22, -2.5)
        time.sleep(5)
        self.movement.grab_object(35, -2.5)
        time.sleep(5)
        self.movement.grab()
        time.sleep(2)
        self.movement.grab_object(30, 15)
        time.sleep(4)
        self.movement.move_servo("1,600")
        self.movement.move_servo("2,50")
        self.movement.move_servo("3,800")
    
        input()

    def handle_message(self, message):
        j = json.loads(message)
        type = j["type"]
        # Choose appropriate movement command
        if(type == "move_motor"):
            move = j["message"]["move"]
            self.movement.move(move)
        elif(type == "move_arm"):
            move = j["message"]["move"]
            self.movement.move(move, "arm")
        elif(type == "toggle_dance"):
            value = j["message"]["value"]
            self.movement.dancing = value
        elif(type == "grab_object"):
            distance = j["message"]["distance"]
            self.movement.grab_object(distance)
        elif(type == "toggle_ai"):
            value = j["message"]["value"]
            print("AI_Socket")
            
    def send(self, json):
        self.messages.append(json)
