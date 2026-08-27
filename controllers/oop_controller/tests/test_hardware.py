import sys
from pathlib import Path
# put src directory on path
src_dir = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(src_dir))

import unittest
from unittest.mock import MagicMock
import math
import hardware

class TestDevice(unittest.TestCase):
    """goal of Device function is to initialise a hardware device"""
    def setUp(self):
        self.mock_robot = MagicMock()
        self.mock_hardware_device = MagicMock()
        self.device_name = "test_device"

    def test_given_valid_inputs_when_initialised_then_has_correct_values(self):
        """Test if initialises with correct values."""
        device = hardware.Device(robot=self.mock_robot,
                            device_name=self.device_name)

        self.assertEqual(device.device_name, self.device_name)
        self.mock_robot.getDevice.assert_called_once_with(self.device_name)

    def test_given_incorrect_robot_type_when_initialised_then_raises_error(
            self):
        """Test output of incorrect robot type."""
        with self.assertRaises(AttributeError):
            # TODO: list of tests as below
            hardware.Device(robot="robot", device_name=self.device_name)
            hardware.Device(robot=None, device_name=self.device_name)
            hardware.Device(robot=float("nan"), device_name=self.device_name)

class TestSensor(unittest.TestCase):
    def setUp(self):
        self.mock_robot = MagicMock()
        self.sensor_name = "test_sensor"
        self.timestep = 32

    def test_given_valid_inputs_when_initialised_then_has_correct_values(self):
        """Test if initialises with correct values."""
        sensor = hardware.Sensor(robot=self.mock_robot, device_name=self.sensor_name,
                                        timestep = self.timestep)
        self.assertEqual(sensor.device_name, self.sensor_name)
        self.assertEqual(sensor.robot, self.mock_robot)
        self.assertEqual(sensor.timestep, self.timestep)
        self.mock_robot.getDevice.assert_called_once_with(self.sensor_name)

class TestDistSensor(unittest.TestCase):
    #TODO: should I use test inheritance?
    def setUp(self):
        self.mock_robot = MagicMock()
        self.sensor_name = "test_sensor"
        self.timestep = 32

    # n.b. Gemini helped with this
    def _create_sensor(self, dist_value, offset):
        """Factory helper: returns a fresh sensor and its mock device."""
        mock_device = MagicMock()
        mock_device.getValue.return_value = dist_value
        sensor = hardware.DistSensor(robot=self.mock_robot,
                            device_name=self.sensor_name,
                            timestep=self.timestep,
                            offset=offset
                            )
        sensor.device = mock_device
        return sensor

    def test_numerical_inputs_when_run_get_distance_then_has_correct_value(
            self):
        test_cases = [
            # (dist_value, offset, expected_result):
            (0.12345678, 0.036, 0.15945678),
            (0.0, 0.0, 0.0),
            (1.0, -1.0, 0),
            # TODO: fix these (e.g. dist value shouldn't be negative)
            (-1.0, 1.0, 0),
            (-1.0, -1.0, -2.0),
            # ("str", "str", "strstr"),
            (float('inf'), 0.036, float('inf')),
            (0.12345678, float('inf'), float('inf')),
            (True, True, 2)

        ]
        nan_test_cases = [
            (float('nan'), 0.036, float('nan')),
            (0.12345678, float('nan'), float('nan')),
        ]

        for dist_value, offset, expected in test_cases:
            with self.subTest(msg="DistSensor",
                              dist_value=dist_value,
                              offset=offset):
                sensor = self._create_sensor(dist_value=dist_value,
                                                offset=offset)
                self.assertEqual(sensor.get_distance(), expected)
        for encoder_value, radius, expected in nan_test_cases:
            with self.subTest(msg="WheelEncoder",
                              encoder_value=encoder_value,
                              radius=radius):
                self.assertTrue(math.isnan(expected))

    def test_non_numerical_inputs_when_run_get_distance_then_has_typeerror(
            self):
        test_cases = [
            # (dist_value, offset):
            (None, 0.036),
            (0.12345678, None),
            (None, None),
            ("str", 0.036),
            (0.12345678, "str"),
        ]
        for dist_value, offset in test_cases:
            with self.subTest(msg="DistSensor",
                              dist_value=dist_value,
                              offset=offset):
                sensor = self._create_sensor(dist_value=dist_value,
                                             offset=offset)
                with self.assertRaises(TypeError):
                    sensor.get_distance()

class TestEncoder(unittest.TestCase):
    def setUp(self):
        self.mock_robot = MagicMock()
        self.sensor_name = "test_sensor"
        self.timestep = 32
    # TODO: align with DRY
    def _create_sensor(self, encoder_value, radius):
        """Factory helper: returns a fresh sensor and its mock device."""
        mock_device = MagicMock()
        mock_device.getValue.return_value = encoder_value
        sensor = hardware.WheelEncoder(robot=self.mock_robot,
                            device_name=self.sensor_name,
                            timestep=self.timestep,
                            wheel_radius=radius
                            )
        sensor.device = mock_device
        return sensor

    def test_numerical_inputs_when_run_get_distance_then_has_correct_value(
            self):
        test_cases = [
            # (encoder_value, radius, expected_result)
            (0.12345678, 0.028, 0.00345678984),
            (0.0, 0.0, 0.0),
            (-1.0, 1.0, -1),

            # TODO: fix these. n.b. radius validation should be handled in
            #  config dataclass
            (1.0, -1.0, -1.0),  # shouldn't be negative radius
            (-1.0, -1.0, 1.0), # shouldn't be negative radius
            (float('inf'), 0.036, float('inf')),
            (0.12345678, float('inf'), float('inf')), # radius cannot be
            # infinite
        ]
            # TODO: fix these
        nan_test_cases = [
            (float('nan'), 0.036, float('nan')),
            (0.12345678, float('nan'), float('nan')),
        ]

        # TODO: align with DRY
        for encoder_value, radius, expected in test_cases:
            with self.subTest(msg="WheelEncoder",
                              encoder_value=encoder_value,
                              radius=radius):
                sensor = self._create_sensor(encoder_value=encoder_value,
                                                radius=radius)
                self.assertEqual(sensor.get_distance(), expected)

        for encoder_value, radius, expected in nan_test_cases:
            with self.subTest(msg="WheelEncoder",
                              encoder_value=encoder_value,
                              radius=radius):
                self.assertTrue(math.isnan(expected))

    def test_non_numerical_inputs_when_run_get_distance_then_has_typeerror(
            self):
        test_cases = [
            # (dist_value, offset)
            (None, 0.036),
            (0.12345678, None),
            (None, None),
            # ("str", 0.036),
            # (0.12345678, "str"),
            # ("str", "str"),
            # (True, True),
            (float('nan'), 0.036), # assume NaN
        ]
        for encoder_value, radius in test_cases:
            with self.subTest(msg="WheelEncoder",
                              encoder_value=encoder_value,
                              radius=radius):
                sensor = self._create_sensor(encoder_value=encoder_value,
                                                radius=radius)
                with self.assertRaises(TypeError):
                    sensor.get_distance()

# TODO: add given_valid_inputs_when_initialised_then_ tests for actuators,
#  individual sensor types

if __name__ == "__main__":
    unittest.main()