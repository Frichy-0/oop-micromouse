"""Unittests for hardware.py"""
import sys
from pathlib import Path

from hardware import DistSensor, WheelEncoder

# put src directory on path
src_dir = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(src_dir))

import unittest
from unittest.mock import MagicMock
import hardware

class TestDevice(unittest.TestCase):
    """Test hardware device initialisation and correct attribute assignment."""
    def setUp(self):
        self.mock_robot = MagicMock()
        self.mock_hardware_device = MagicMock()
        self.device_name = "test_device"

    def test_given_valid_inputs_when_initialised_then_has_correct_values(self):
        """Test if initialises with input values."""
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
    """Test enabling sensor device and correct attribute assignment."""
    def setUp(self):
        self.mock_robot = MagicMock()
        self.sensor_name = "test_sensor"
        self.timestep = 32

    def test_given_valid_inputs_when_initialised_then_has_correct_values(self):
        """Test if Sensor correctly initialises with input values."""
        sensor = hardware.Sensor(robot=self.mock_robot, device_name=self.sensor_name,
                                        timestep = self.timestep)
        self.assertEqual(sensor.device_name, self.sensor_name)
        self.assertEqual(sensor.robot, self.mock_robot)
        self.assertEqual(sensor.timestep, self.timestep)
        sensor.device.enable.assert_called_once_with(self.timestep)

class TestDistSensor(unittest.TestCase):
    """Test correct offset assignment and verify distance calculation logic."""
    #TODO: should I use test inheritance?
    def setUp(self):
        self.mock_robot = MagicMock()
        self.sensor_name = "test_sensor"
        self.timestep = 32
        self.offset = 1
        self.sensor = DistSensor(robot=self.mock_robot,
                            device_name=self.sensor_name,
                            timestep=self.timestep,
                            offset=self.offset
                            )

    # n.b. Gemini helped with this
    def _create_sensor(self, dist_value, offset):
        """Factory helper: returns a fresh sensor and its mock device."""
        mock_device = MagicMock()
        mock_device.getValue.return_value = dist_value
        sensor = hardware.DistSensor(
                            robot=self.mock_robot,
                            device_name=self.sensor_name,
                            timestep=self.timestep,
                            offset=offset
                            )
        sensor.device = mock_device
        return sensor

    def test_given_valid_inputs_when_initialised_then_sets_offset(self):
        """Test if DistSensor correctly assigns offset attribute."""
        self.assertEqual(self.sensor.offset, self.offset)

    def test_when_call_get_distance_then_calls_value(self):
        """Test if get_distance fetches a reading from the connected
        hardware device."""
        self.sensor.get_distance()
        self.sensor.device.getValue.assert_called_once()

    def test_numerical_inputs_when_run_get_distance_then_has_correct_value(
            self):
        """
        Verify that DistSensor.get_distance() calculates correct values across
        various numerical inputs.
        Tests standard floats, zero, negative values, positive infinity,
        boolean coercion.
        """
        test_cases = [
            # (dist_value, offset, expected_result):
            (0.12345678, 0.036, 0.15945678),
            (0.0, 0.0, 0.0),
            (1.0, -1.0, 0),
            # TODO: decide how to handle these in the code (e.g. dist value
            #  shouldn't be negative)
            (-1.0, 1.0, 0),
            (-1.0, -1.0, -2.0),
            (float('inf'), 0.036, float('inf')),
            (0.12345678, float('inf'), float('inf')),
            (True, True, 2),
        ]
        for dist_value, offset, expected in test_cases:
            with self.subTest(msg="DistSensor",
                              dist_value=dist_value,
                              offset=offset):
                sensor = self._create_sensor(dist_value=dist_value,
                                                offset=offset)
                self.assertEqual(sensor.get_distance(), expected)

    def test_non_numerical_inputs_when_run_get_distance_then_has_typeerror(
            self):
        """
        Verify that DistSensor.get_distance() raises TypeError across various
        non-numerical inputs.
        Tests none, strings, NaN.
        """
        test_cases = [
            # (dist_value, offset):
            (None, 0.036),
            (0.12345678, None),
            (None, None),
            ("str", 0.036),
            (0.12345678, "str"),
            ("str", "str"),
            (float('nan'), 0.036),
            (0.12345678, float('nan')),
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
    """Test correct radius assignment and verify distance calculation logic."""
    def setUp(self):
        self.mock_robot = MagicMock()
        self.sensor_name = "test_sensor"
        self.timestep = 32
        self.radius = 1
        self.sensor = WheelEncoder(robot=self.mock_robot,
                            device_name=self.sensor_name,
                            timestep=self.timestep,
                            wheel_radius=self.radius
                            )
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

    def test_given_valid_inputs_when_initialised_then_sets_radius(self):
        """Test if WheelEncoder correctly assigns radius attribute."""
        self.assertEqual(self.sensor.radius, self.radius)

    def test_when_call_get_distance_then_calls_value(self):
        """Test if get_distance fetches a reading from the connected
        hardware device."""
        self.sensor.get_distance()
        self.sensor.device.getValue.assert_called_once()

    def test_numerical_inputs_when_run_get_distance_then_has_correct_value(
            self):
        """
        Verify that WheelEncoder.get_distance() calculates correct values
        across various numerical inputs.
        Tests standard floats, zero, negative values, positive infinity,
        boolean coercion.
        """
        test_cases = [
            # (encoder_value, radius, expected_result)
            (0.12345678, 0.028, 0.00345678984),
            (0.0, 0.0, 0.0),
            (-1.0, 1.0, -1),
            # TODO: decide how to handle these in the code
            (1.0, -1.0, -1.0),  # shouldn't be negative radius
            (-1.0, -1.0, 1.0), # shouldn't be negative radius
            (float('inf'), 0.036, float('inf')),
            (0.12345678, float('inf'), float('inf')), # radius cannot be
            # infinite
            (True, True, 1),
        ]
        # TODO: align with DRY
        for encoder_value, radius, expected in test_cases:
            with self.subTest(msg="WheelEncoder",
                              encoder_value=encoder_value,
                              radius=radius):
                sensor = self._create_sensor(encoder_value=encoder_value,
                                                radius=radius)
                self.assertEqual(sensor.get_distance(), expected)

    def test_non_numerical_inputs_when_run_get_distance_then_has_typeerror(
            self):
        """
        Verify that WheelEncoder.get_distance() raises TypeError across various
        non-numerical inputs.
        Tests none, strings, NaN.
        """
        test_cases = [
            # (dist_value, offset)
            (None, 0.036),
            (0.12345678, None),
            (None, None),
            # TODO: decide how to handle these in the code
            ("str", 0.036),
            (0.12345678, "str"),
            ("str", "str"),
            (float('nan'), 0.036),
            (0.12345678, float('nan')),
        ]
        for encoder_value, radius in test_cases:
            with self.subTest(msg="WheelEncoder",
                              encoder_value=encoder_value,
                              radius=radius):
                sensor = self._create_sensor(encoder_value=encoder_value,
                                                radius=radius)
                with self.assertRaises(TypeError):
                    sensor.get_distance()

class TestDriveMotor(unittest.TestCase):
    """Test correct method call for set_position and set_velocity methods."""
    def setUp(self):
        self.mock_robot = MagicMock()
        self.device_name = "test_device"
        self.drive_motor = hardware.DriveMotor(robot=self.mock_robot,
                            device_name=self.device_name)

    def test_given_valid_inputs_when_set_position_then_has_correct_values(
            self):
        """Test if set_position writes input values to connected hardware
        device"""
        position = 10
        self.drive_motor.set_position(position)
        self.drive_motor.device.setPosition.assert_called_once_with(position)

    def test_given_valid_inputs_when_set_velocity_then_has_correct_values(
            self):
        """Test if set_velocity writes input values to connected hardware
        device"""
        velocity = 10
        self.drive_motor.set_velocity(velocity)
        self.drive_motor.device.setVelocity.assert_called_once_with(velocity)

# TODO: add DeviceInitialiser tests
class TestDeviceInitialiser(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == "__main__":
    unittest.main()