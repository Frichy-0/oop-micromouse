"""
perception.py

Module that takes sensor data and prior knowledge of the environment as
inputs and outputs the perceived state of the robot and its environment -
wall locations and pose.

"""

from config import WorldConfig, RobotConfig
from hardware import Sensors


# INPUTS: sensor data
# OUTPUTS: perceived state (robot and environment). Wall location and pose.

# TODO: split wall detection and pose estimation to align with single
#  responsibility principle
class Perception:
    def __init__(self, env_config: WorldConfig, robot_config: RobotConfig,
                 sensor:
        Sensors):

        self.sensor = sensor
        self.env_config = env_config
        self.robot_config = robot_config
        self.emergency_dist = self._calc_min_distance()

        self.current_pose = (self._grid_to_world(self.env_config.start_cell) +
                                    (self.env_config.start_direction,))
        print(f"estimated pose at initialisation: {self.current_pose}")

        # TODO: assign max number of entries. Switch to dict with timestamps?
        self.hist_ds_readings = []

    # NOTE: run this every tick
    def update(self):
        print(self.update_ds_readings())
        print(self._detect_walls())

    def _calc_min_distance(self) -> float:
        """calculates the safe minimum distance from an obstacle"""
        # TODO: replace placeholder with calculation
        return 0.5

    # CRITICAL: we want a single source of distance readings -
    # currently done by updating init.
    def update_ds_readings(self) -> dict[str, int]:
        # NOTE: attempting to balance good code design with minimising
        # failure points when triggering emergency stop. Emergency stop is
        # in perception.py rather than hardware.py to keep the architecture
        # flexible but at the expense of reliability. To compensate, a single
        # function with several tasks is used instead of increasing
        # structural complexity by passing between functions.
        # TODO: ensure safeguards to compensate for extra abstraction

        # TODO: ensure that emergency stop is handled in a way that allows
        #  readings to continue to be logged. Threading?
        front = self.sensor.ds_front.get_distance()
        if front < self.emergency_dist:
            self.trigger_emergency_stop()

        # TODO: map the sensor readings to the angle of the sensors instead
        #  of direction
        ds_readings = {
            "front": front,
            "back": self.sensor.ds_back.get_distance(),
            "left": self.sensor.ds_left.get_distance(),
            "right": self.sensor.ds_right.get_distance()
        }

        self.hist_ds_readings.append(ds_readings)
        return ds_readings

    def trigger_emergency_stop(self):
        print(f"EMERGENCY STOP PLACEHOLDER")

    def _detect_walls(self) -> dict[str, int]:
        """Detect current walls based on distance from robot."""
        # TODO: ensure it always has the latest DS values to do this. Do via
        #  timestamp? architecture?
        walls = {}
        # TODO: cycle through looking for acceptable readings?
        latest_reading = self.hist_ds_readings[-1]
        for direction, value in latest_reading.items():
            # wall assumed to belong to cell if distance is less than the
            # diagonal width of the cell minus the wall's ingress into the
            # cell.
            # TODO: find a more sophisticated method
            if (value*2 < self.env_config.cell_diagonal -
                    self.env_config.wall_width/2):
                walls[direction] = 1
            else:
                walls[direction] = 0
        return walls

    # TODO: this function also called during path planning - refactor
    def _grid_to_world(self, cell) -> tuple[int, int]:
        """ Converts grid coordinates to cartesian centre of cell."""
        # TODO: centre calculated asit is assumed that the robot will always
        #  aim for the centre of the cell. For more sophisticated movement
        #  strategies could return cell corner coordinates, perhaps
        #  calculated at initialisation?

        # given environment is a square and cartesian origin is in the centre:
        # -length of environment edge in metres/2 finds the lower bound
        # coordinate values of the grid domain
        # TODO: refactor to avoid calculating every time?
        lower_bound = -(self.env_config.grid_size *
                         self.env_config.cell_edge_l) / 2

        # get cartesian value of lower edge of cell
        x = lower_bound + cell[0] * self.env_config.cell_edge_l
        y = lower_bound + cell[1] * self.env_config.cell_edge_l

        # add half the cell length to both values to get the centre
        x = x + self.env_config.cell_edge_l / 2
        y = y + self.env_config.cell_edge_l / 2
        return x, y

