class ControlState:
    def __init__(self):
        self.status = "controlState"
        self.ai = None
        self.vision = None

    def start(self):
        print(self.status)

    def end(self):
        print("end")
