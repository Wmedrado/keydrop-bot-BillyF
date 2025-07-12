import sys
from pathlib import Path
import tempfile
import unittest

# Allow imports from package root
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.backend.config.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.manager = ConfigManager(config_dir=self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_default_config_created(self):
        config = self.manager.get_config()
        self.assertEqual(config.num_tabs, 5)
        self.assertTrue((Path(self.tmp.name) / 'bot_config.json').exists())

    def test_update_and_persist(self):
        self.manager.update_config(num_tabs=3, execution_speed=2.5)
        config = self.manager.get_config()
        self.assertEqual(config.num_tabs, 3)
        self.assertEqual(config.execution_speed, 2.5)

        reload_mgr = ConfigManager(config_dir=self.tmp.name)
        self.assertEqual(reload_mgr.get_config().num_tabs, 3)

    def test_reset_defaults(self):
        self.manager.update_config(num_tabs=10)
        self.manager.reset_to_defaults()
        config = self.manager.get_config()
        self.assertEqual(config.num_tabs, 5)


if __name__ == '__main__':
    unittest.main()
