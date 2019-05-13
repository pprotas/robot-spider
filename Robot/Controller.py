from Communication import Communication


class Controller:

    def __init__(self):
        print("controller started")
        communication = Communication(self)
        communication.start()

    def notify(self, message):
        print(message)


if __name__ == '__main__':
    controller = Controller()

