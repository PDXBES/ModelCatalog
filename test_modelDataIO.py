from unittest import TestCase
import mock
import os
from model_data_io import ModelDataIO
from model import Model
from simulation import Simulation
from config import Config


class TestModelDataIO(TestCase):

    def setUp(self):
        self.config = Config()
        self.modeldataio = ModelDataIO(self.config)
        self.mock_model = mock.MagicMock(Model)
        self.mock_model.model_path = r"C:\model_path"

    @mock.patch("os.walk")
    def test_read_simulations_calls_os_walk(self, mock_os_walk):

        self.modeldataio.read_simulations(self.mock_model)
        self.assertTrue(mock_os_walk.called)

    @mock.patch("os.walk")
    def test_read_simulation_reads_standard_simulation_returns_simulation_object(self, mock_os_walk):

        mock_os_walk.return_value = iter([("path", ["D25yr6h"], "file name")])
        list_of_simulations = self.modeldataio.read_simulations(self.mock_model)
        first_simulation = list_of_simulations[0]  # type: Simulation
        self.assertEquals(first_simulation.model_path, r"C:\model_path")
        self.assertEquals(first_simulation.dev_scenario_id, 0)
        self.assertEquals(first_simulation.storm_id, 1)
        self.assertEquals(first_simulation.sim_desc, "D25yr6h")