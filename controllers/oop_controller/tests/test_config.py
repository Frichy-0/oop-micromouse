

import sys
from pathlib import Path
# put src directory on path
src_dir = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(src_dir))

import unittest
from config import RobotConfig

# Placeholder test
class TestRobotConfig(unittest.TestCase):
    def setUp(self):
        self.robot_config = RobotConfig(32, 32)
    def test_config_values(self):
        self.assertEqual(self.robot_config.sim_timestep, 32)