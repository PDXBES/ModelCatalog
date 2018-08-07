from unittest import TestCase
import mock
from config import Config


class TestConfig(TestCase):
    def setUp(self):
        self.config = Config()

    def test_storm_dict_return_correct_value_for_storm(self):
        storm_name, storm_type = self.config.storm[0]
        self.assertEquals(storm_name, "user_def")
        self.assertEquals(storm_type, "U")

    def test_dev_scenario_dict_return_correct_value(self):
        dev_scenario = self.config.dev_scenario
        self.assertEquals(dev_scenario[0], "EX")



