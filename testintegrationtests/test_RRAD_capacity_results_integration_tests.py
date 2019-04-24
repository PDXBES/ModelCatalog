from unittest import TestCase
from dataio.simulation_data_io import SimulationDataIO
from businessclasses.config import Config
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from businessclasses.simulation import Simulation
import mock
import unittest

test_flag = "TEST"
class TestRRADCapacityResults(TestCase):

    def setUp(self):

        self.config = Config(test_flag)
        self.model_catalog_db_data_io = ModelCatalogDbDataIo(self.config)
        self.simulation_data_io = SimulationDataIO(self.config, self.model_catalog_db_data_io)
        self.simulation = Simulation(self.config)
        self.simulation.id = 999998
        self.simulation.storm_id = 1

        self.patch_simulation_path = mock.patch.object(self.simulation, "path")
        self.mock_simulation_path = self.patch_simulation_path.start()

        self.mock_simulation_path.return_value = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\Test_Cases\Taggart\BaseR011018V4ic\sim\D25yr6h"

    def tearDown(self):
        self.mock_simulation_path = self.patch_simulation_path.stop()

    def test_add_simulation_results(self):
        self.simulation_data_io.add_simulation_results(self.simulation, None)

