from unittest import TestCase
import mock
from mock_config import MockConfig
from businessclasses.area_results import AreaResults
from businessclasses.simulation import Simulation

class TestArea(TestCase):

    def setUp(self):
        mock_config = MockConfig()

        self.mock_simulation = mock.MagicMock(Simulation)
        self.mock_simulation.storm_id = 1
        self.area = AreaResults(mock_config.config)




