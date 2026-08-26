"""
This modules holds the robot and environment configuration data used by the
robot controller.
"""

from dataclasses import dataclass, fields
import numpy as np
from typeguard import check_type

# TODO: make less messy? - generates attributes objects don't need.
@dataclass(frozen=True)
class DeviceConfig:
    """dataclass to assist device configuration"""
    device_name: str
    timestep: int = None
    offset: float = None
    angle: float = None
    wheel_radius: float = None

@dataclass(frozen=True)
class RobotConfig:
    sim_timestep: int
    control_timestep: int
    wheel_radius: float = 0.02  # metres
    wheel_offset: float = 0.028  # metres (measured from centre)
    max_speed: float = 6.28  # rad/s # TODO: switch to m/s for consistency?
    ds_offset: float = 0.035

    # TODO: move to __post_init__?
    @property
    def devices(self) -> dict[str, DeviceConfig]:
        """Central registry for all robot devices."""
        # NOTE: keys map directly to names in hardware.py container classes
        return {
            "ds_front": DeviceConfig(
                device_name="front_ds",
                offset=self.ds_offset,
                timestep=self.control_timestep,
                angle=0
            ),
            "ds_back": DeviceConfig(
                device_name="rear_ds",
                offset=self.ds_offset,
                timestep=self.control_timestep,
                angle=3.14
            ),
            "ds_left": DeviceConfig(
                device_name="left_ds",
                offset=self.ds_offset,
                timestep=self.control_timestep,
                angle= 1.57
            ),
            "ds_right": DeviceConfig(
                device_name="right_ds",
                offset=self.ds_offset,
                timestep=self.control_timestep,
                angle=-1.57
            ),
            "encoder_l": DeviceConfig(
                device_name="left wheel sensor",
                wheel_radius=self.wheel_radius,
                timestep=self.control_timestep,
            ),
            "encoder_r": DeviceConfig(
                device_name="right wheel sensor",
                wheel_radius=self.wheel_radius,
                timestep=self.control_timestep,
            ),
            "motor_l": DeviceConfig(
                device_name="left wheel motor",
            ),
            "motor_r": DeviceConfig(
                device_name="right wheel motor",
            ),
        }

    def __post_init__(self):
        self.validate_timestep()
        self.validate_type()

    def validate_timestep(self):
        """Generates a warning if timesteps don't align"""
        # TODO: test this
        if self.control_timestep % self.sim_timestep != 0:
            logging.warning("Robot timestep is not a multiple of basic "
                            "timestep. Webots will round to nearest timestep")
    def validate_type(self):
        """Raises error if attribute is wrong type"""
        # TODO: test this
        for f in fields(self):
            value = getattr(self, f.name)
            check_type(value, f.type)

@dataclass(frozen=True)
class WorldConfig:
    """dataclass containing robot's prior knowledge of the environment"""
    grid_size: int = 4
    goal_cell: tuple[int, int] = (0,0)
    start_cell: tuple[int, int] = (3,3)
    start_direction: float = -np.pi / 2
    cell_edge_l: float  = 0.25
    wall_width: float = 0.01

    @property
    def cell_diagonal(self) -> float:
        return np.sqrt(2 * (self.cell_edge_l ** 2)) - (self.wall_width / 2)

