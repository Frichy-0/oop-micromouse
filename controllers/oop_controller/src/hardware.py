"""
Module to encapsulate and initialise robot hardware devices.
"""

import logging
import math
import inspect

from dataclasses import dataclass, fields, asdict
from controller import Robot
from src.config import RobotConfig

# =============================================================================
# DEVICES
# =============================================================================
class Device:
    """Parent class for all devices. Connects software to the device"""
    def __init__(self, robot: Robot, device_name: str):
        self.robot = robot
        self.device_name = device_name
        self.device = self.robot.getDevice(device_name)
        logging.debug(f"{self.device_name}: getDevice has been initialised "
                      f"as object {self.device}")

# -----------------------------------------------------------------------------
# Sensors
# -----------------------------------------------------------------------------
class Sensor(Device):
    """Parent class for sensors. Enables sensors and assigns timestep"""
    # TODO: have getValue/s method here and use polymorphism in subclasses?
    def __init__(self, robot, device_name, timestep: int):
        super().__init__(robot, device_name)
        self.timestep = timestep
        self.device.enable(self.timestep)
        logging.debug(f"{self.device_name} has been enabled "
                      f"with a timestep of {self.timestep}.")

class DistSensor(Sensor):
    def __init__(self, robot, device_name, timestep, offset: float):
        super().__init__(robot, device_name, timestep)
        self.offset = offset # abs value offset from centre of the robot

    def get_distance(self) -> float:
        # TODO: do i want with offset or raw value? e.g. a real sensor's
        #  performance might vary according to distance so raw value
        #  is needed.
        distance = self.device.getValue() + self.offset
        if math.isnan(distance):
            raise TypeError(
                f"Expected float for {self.device_name}, got NaN")
        return distance

class WheelEncoder(Sensor):
    def __init__(self, robot, device_name, wheel_radius, timestep):
        super().__init__(robot, device_name, timestep)
        # TODO: belong in a different class, like hardware?
        self.radius = wheel_radius

    def get_distance(self) -> float: # returns distance in metres
        enc_value = self.device.getValue()
        # TODO: if m to radians used elsewhere consider a separate function
        # convert to metres to ensure consistent units
        distance = enc_value * self.radius
        if math.isnan(distance):
            raise TypeError(
                f"Expected float for {self.device_name}, got NaN")
        return distance

# -----------------------------------------------------------------------------
# Actuators
# -----------------------------------------------------------------------------
class DriveMotor(Device):
    def __init__(self, robot, device_name):
        super().__init__(robot, device_name)

    def set_position(self, position):
        self.device.setPosition(position)

    def set_velocity(self, vel):
        self.device.setVelocity(vel)

# =============================================================================
# DEVICE CONTAINERS
# =============================================================================
@dataclass
class Sensors:
    ds_front: DistSensor
    ds_back: DistSensor
    ds_left: DistSensor
    ds_right: DistSensor
    encoder_l: WheelEncoder
    encoder_r: WheelEncoder

@dataclass
class Actuators:
    motor_l: DriveMotor
    motor_r: DriveMotor

# =============================================================================
# DEVICE INITIALISATION LOGIC
# =============================================================================

class DeviceInitialiser:
    """Factory class to handle initialisation of device objects."""
    def __init__(self, robot: Robot, config: RobotConfig):
        self.robot = robot
        self.config = config

    def _initialise(self, container_obj):
        """initialises all objects in a container class"""
        # TODO: currently uses DeviceConfig in hardware.py to retrieve
        #  config values which returns redundant parameters. Think through
        #  potential ramifications of this design choice.
        obj_instances = {}

        for f in fields(container_obj):  # retrieve field data for object
            # f.name = device variable name - see dataclass container
            # f.type = name of the class, e.g. DriveMotor
            kwargs = {}

            # retrieve preconfigured names and values for device
            spec = asdict(self.config.devices[f.name])

            # retrieve constructor parameters of the device's class
            params = list(inspect.signature(f.type).parameters.keys())

            # assign configuration values to constructor parameter names
            for param in params:
                # TODO: add timestep validation logic. Other validation logic?
                if param in spec.keys():
                    kwargs.update({param: spec[param]})

            logging.debug(f"kwarg values for {f.name} are {kwargs}")

            # add initialised object to dictionary of devices
            obj_instances[f.name] = f.type(self.robot, **kwargs)

        logging.debug(f"object dictionary: {obj_instances}")

        # initialise devices in dataclass container via dictionary unpacking
        container = container_obj(**obj_instances)

        logging.info(f"Container initialised: {container_obj}")
        return container

    def create_sensors(self) -> Sensors:
        return self._initialise(Sensors)

    def create_actuators(self) -> Actuators:
        return self._initialise(Actuators)