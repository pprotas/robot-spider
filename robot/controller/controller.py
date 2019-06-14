from communication.server_socket import Server_Socket
from communication.ai_socket import AI_Socket
from communication.i2c import I2C
from movement.movement import Movement, degree_to_position
from threading import Thread
from vision.camera import Camera
import time
import json


class Controller:

    def __init__(self):
        print("Program started")
        self.power = 200
        # Movement center with connection to Arduino
        self.i2c = I2C(self, 4)
        self.movement = Movement(self.i2c)
        self.controltype = None
        self.cloudcomputer = None
        self.server
        self.camera
        self.ai
        
    def start(self):
        # Connection to webserver
        self.server = Server_Socket(self)
        Thread(target=server.start, daemon=True).start()
    #Thread(target=AI_Socket(self).start, daemon=True).start()
        # Status checker
        Thread(target=self.i2c.get_status, daemon=True).start()
        self.camera = Camera()
        Thread(target=self.camera.start()).start() 

        #self.movement.move_servo("2,150")
        #self.movement.move_servo("3,600")
        #time.sleep(5)
        #self.movement.grab_object(22, -2.5)
        #time.sleep(5)
        #self.movement.grab_object(35, -2.5)
        #time.sleep(5)
        #self.movement.grab()
        #time.sleep(2)
        #self.movement.grab_object(30, 15)
        #time.sleep(4)
        #self.movement.move_servo("1,600")
        #self.movement.move_servo("2,50")
        #self.movement.move_servo("3,800")
        
##        while self.power > 170:
##            print(self.power)
##            time.sleep(0.1)
##        print(self.power)
##        raise KeyboardInterrupt
        input()

    def handle_message(self, message):
        j = json.loads(message)
        type = j["type"]
        
        # Handle information message
        if(type == "request"):
            value = j["message"]["value"]
            if message["type"]["message"]["type"] == "image":
                if (message["type"]["message"]["arg"] == "cloudcomputer"):
                    self.camera.requests.append(self.cloudcomputer)
                elif (message["type"]["message"]["arg"] == "server"):
                    self.camera.requests.append(self.server)
        
        # Handle config message
        elif(type == "config"):
            if (j["message"]["controltype"] == "manual"):
                if (self.controltype is not "manual"):
                    self.controltype = "manual"
                    #stop ai and socket
                
            if (j["message"]["controltype"] == "ai"):
                if (self.controltype is not "ai"):
                    self.controltype = "ai"
                    x = {"type": "request", "message": {"type": "image", "arg": "cloudcomputer"}}
                    self.server.messages.append(json.dump(x))
                    self.ai = j["message"]["controlstate"]
        
        # Handle response message
        elif(type == "Response"):
            if (j["message"]["type"] == "visionserver"):
                ip = j["message"]["ip"]
                if (ip is not ""):
                    if(self.controltype == "ai" and self.cloudcomputer == None):
                        self.cloudcomputer = AI_Socket(self, ip)
                        self.cloudcomputer.start()
                        self.cloudcomputer.messages.append("mode "+ self.ai)
                
        # Choose appropriate movement command
        elif(type == "move_motor"):
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
            
    # def send(self, json):
    #     self.messages.append(json)
