"""
This module serves as the entry point to the Webots simulator. It
 holds the control loop coodinator, setup code and the main
 controller loop.
"""
import logging


import sys
from pathlib import Path



# put src directory on path
src_dir = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(src_dir))

from controller import Robot
from hardware import DeviceInitialiser
from config import RobotConfig, WorldConfig
from perception import Perception
from planning import Planner
from action import Mover


# Configure logging 
logging.basicConfig(level=logging.INFO)

class RobotController:
    """
    Mediator class to coordinate the control loop.
    """
    def __init__(self, perception: Perception, planner: Planner, mover:
    Mover):
        self.perception = perception
        self.planner = planner
        self.mover = mover

    def run(self):
        self.perception.update()
        self.planner.update()
        self.mover.update()


if __name__ == "__main__":
    # TODO: tidy initialisations into factory
    print("Initialising...")

    robot = Robot()
    robot_config = RobotConfig(sim_timestep = int(robot.basic_time_step),
                         control_timestep = 32)
    world_config = WorldConfig()

    initialise_devices = DeviceInitialiser(robot, robot_config) # full
    sensors = initialise_devices.create_sensors()
    actuators = initialise_devices.create_actuators()

    perception = Perception(world_config, robot_config, sensors)
    planner = Planner()
    mover = Mover(actuators)

    controller = RobotController(perception, planner, mover)

    print("Start robot")
    while robot.step(robot_config.control_timestep) != -1:
        controller.run()

