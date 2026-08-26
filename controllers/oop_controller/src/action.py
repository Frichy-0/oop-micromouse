from hardware import Actuators

class Mover:
    def __init__(self, actuators: Actuators):
        self.actuator = actuators

        self.actuator.motor_l.set_position(float('inf'))
        self.actuator.motor_r.set_position(float('inf'))

    def update(self):
        pass
