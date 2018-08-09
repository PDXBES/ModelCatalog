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

    def test_standard_simulation_names(self):
        standard_simulation_names = ['D25yr6h', 'D25yr6h-50', 'D25yr6h-BO', 'D10yr6h', 'D10yr6h-50', 'D10yr6h-BO']
        output_simulation_names = self.config.standard_simulation_names()
        self.assertEquals(output_simulation_names, standard_simulation_names)



