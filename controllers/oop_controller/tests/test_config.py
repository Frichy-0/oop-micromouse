"""Unittests for config.py"""

import sys
from pathlib import Path
# put src directory on path
src_dir = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(src_dir))

import unittest
from config import RobotConfig

class TestRobotConfig(unittest.TestCase):
    def setUp(self):
        pass
    def test_given_valid_timestep_multiple_when_instantiate_then_no_warning(self):
        """Test no warning if correct timestep multiple is given"""
        test_cases = [
            # (sim_timestep, control_timestep)
            (32, 32),
            (16, 32),
            # TODO: create tests
            # (-1, 1),
            # (1, -1),
            # (-1, -1),
            # (0, 0),
            # (0, 32),
            # also test: none, NaN, inf, str
        ]

        # TODO: test against the actual simulation to see what the outcome is
        for sim_timestep, ctrl_timestep in test_cases:
            with self.subTest(msg="RobotConfig valid timestep",
                              sim_timestep=sim_timestep,
                              control_timestep=ctrl_timestep):
                with self.assertNoLogs(level='WARNING'):
                    RobotConfig(sim_timestep=sim_timestep, control_timestep=ctrl_timestep)

    def test_given_invalid_timestep_multiple_when_instantiate_return_warning(self):
        """Test warning if incorrect timestep multiple is given"""
        test_cases = [
            # (sim_timestep, control_timestep)
            (32, 16),
            (15, 32),
        ]

        # TODO: test timestep validation in isolation?
        # TODO: test against the actual simulation to see what the outcome is
        for sim_timestep, ctrl_timestep in test_cases:
            with self.subTest(msg="RobotConfig invalid timestep multiple",
                              sim_timestep=sim_timestep,
                              control_timestep=ctrl_timestep):
                with self.assertLogs(level='WARNING'):
                    RobotConfig(sim_timestep=sim_timestep, control_timestep=ctrl_timestep)


    # TODO: RobotConfig tests:
    #   - add additional error cases if relevant
    #   - add range tests
    #   - add type validation tests
    #   - add devices() tests
    # TODO: test against the actual simulation to see what the outcome is
    # TODO: WorldConfig tests, DeviceConfig tests


