from robot.state.controlState.controlState import ControlState


class StairState(ControlState):
    def __init__(self):
        self.status = "stairState"
