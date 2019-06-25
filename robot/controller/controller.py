from communication.server_socket import Server_Socket
from communication.ai_socket import AI_Socket
from communication.i2c import I2C
from movement.movement import Movement, degree_to_position
from movement.movement import SingleDance
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
        self.singledance = SingleDance()
        self.controltype = None
        self.cloudcomputer = None
        self.server = None
        self.camera = None
        self.ai = None
        
    def start(self):
        # Connection to webserver
        self.server = Server_Socket(self)
        Thread(target=self.server.start, daemon=True).start()
        # Status checker
        Thread(target=self.i2c.get_status, daemon=True).start()
        self.camera = Camera(self)
        Thread(target=self.camera.start).start() 
        self.movement.set_speed(100)
        self.movement.fold_legs()
        

##        while self.power > 170:
##            print(self.power)
##            time.sleep(0.1)

        input()

    def handle_message(self, message):
        j = json.loads(message)
        type = j["type"]
        #print(message)
        
        # Handle information message
        if(type == "request"):
            if j["message"]["type"] == "image":
                if (j["message"]["arg"][0] == "cloudcomputer"):
                    self.camera.requests.append(self.cloudcomputer)
                elif (j["message"]["arg"][0] == "server"):
                    print("camera:")
                    self.camera.stream(j["message"]["arg"][1], 0.05)
        
        # Handle config message
        elif(type == "config"):
            if (j["message"]["controltype"] == "manual"):
                if (self.controltype != "manual"):
                    self.controltype = "manual"
                    x = {"type": "config", "message": {"controltype": "done", "controlstate": False}}
                    self.cloudcomputer.messages.append(json.dumps(x))
                    
                #check if controlstate is a dance
                if (j["message"]["controlstate"] == 'singledance'):
                    # start singledance
                    Thread(target=self.singledance.start(), daemon=True).start()
                
            elif (j["message"]["controltype"] == "ai"):
                if (self.controltype != "ai"):
                    self.controltype = "ai"
                    x = {"type": "request", "message": {"type": "visionserver", "arg": "lock"}}
                    self.server.messages.append(json.dumps(x))
                    self.ai = j["message"]["controlstate"]
                else:
                    self.ai = j["message"]["controlstate"]
                    x = {"type": "config", "message": {"controltype": "ai", "controlstate": self.ai} }
                    self.cloudcomputer.messages.append(json.dumps(x))

            elif (j["message"]["controltype"] == "done"):
                self.ai = ""
                self.controltype = "manual"
                #turn off current robot actions
                handle_message()
                self.cloudcomputer.messages = []
                self.cloudcomputer.messages.append(j)

            elif (j["message"]["controltype"] == "close"):
                if(self.cloudcomputer != None):
                    self.cloudcomputer.ws.close()
                    self.cloudcomputer = None
                    self.ai = None
                    print("cloudcomputer disconnected")
                    x =  x = {"type": "config", "message": {"controltype": "done", "controlstate": j["message"]["controlstate"]} }
                    self.server.messages.append(j)
    
            #in theory not used:     
            elif (j["message"]["controltype"] == "capture"):
                if(self.cloudcomputer != None):
                    print("send camera config to cloudcomputer")
                    self.cloudcomputer.messages.append(json.dumps(j))
            #------------------
        
        # Handle response message
        elif(type == "response"):
            if (j["message"]["type"] == "visionserver"):
                ip = j["message"]["ip"]
                if (ip != ""):
                    if(self.controltype == "ai" and self.cloudcomputer == None):
                        self.cloudcomputer = AI_Socket(self, ip)
                        Thread(target=self.cloudcomputer.start, daemon=True).start()
                        x = {"type": "config", "message": {"controltype": "ai", "controlstate": self.ai}}
                        self.cloudcomputer.messages.append(json.dumps(x))
                else:
                    self.controltype = ""
                    self.ai = ""
                    x = {"type": "config", "message": {"controltype": "done", "controlstate": False }}
                    self.server.append(json.dumps(x))
                
        # Choose appropriate movement command
        elif(type == "move_motor"):
            print("Moving motor")
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
            self.movement.grab_object(34, -6)
            self.movement.support()
        elif(type == "drop_object"):
            distance = j["message"]["distance"]
            self.movement.drop_object()
        elif(type == "fold_legs"):
            self.movement.fold_legs()
        elif(type == "tilt_front"):
            self.movement.tilt_front()
        elif(type == "tilt_back"):
            self.movement.tilt_back()


