from unittest import TestCase
from simulation_data_io import SimulationDataIO
from config import Config
from model_catalog_db_data_io import ModelCatalogDbDataIo
from simulation import Simulation
import mock
import unittest

#@unittest.skip("Integration Tests")
class TestRRADCapacityResults(TestCase):

    def setUp(self):
        self.config = Config()
        self.model_catalog_db_data_io = ModelCatalogDbDataIo(self.config)
        self.simulation_data_io = SimulationDataIO(self.config, self.model_catalog_db_data_io)
        self.simulation = Simulation(self.config)
        self.simulation.id = 888887
        self.simulation.storm_id = 1

        self.patch_simulation_path = mock.patch.object(self.simulation, "path")
        self.mock_simulation_path = self.patch_simulation_path.start()

        self.mock_simulation_path.return_value = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\Test_Cases\Taggart\BaseR011018V4ic\sim\D25yr6h"

    def tearDown(self):
        self.mock_simulation_path = self.patch_simulation_path.stop()

    def test_append_area_results_to_db(self):
        self.simulation.create_areas(self.simulation_data_io)
        self.simulation_data_io.append_area_results_to_db(self.simulation.areas)

