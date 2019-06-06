
from businessclasses.model_catalog import ModelCatalog
from businessclasses.model import Model
from dataio.model_data_io import ModelDataIo
import getpass
import datetime
from unittest import TestCase
from dataio.simulation_data_io import SimulationDataIo
from businessclasses.config import Config
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from dataio.rrad_db_data_io import RradDbDataIo
from businessclasses.simulation import Simulation
import mock
import unittest

test_flag = "TEST"
class TestRRADCapacityResults(TestCase):

    def setUp(self):

        self.config = Config(test_flag)
        self.model_catalog_db_data_io = ModelCatalogDbDataIo(self.config)
        self.rrad_db_data_io = RradDbDataIo(self.config)
        self.simulation_data_io = SimulationDataIo(self.config, self.model_catalog_db_data_io)
        self.simulation = Simulation(self.config)
        self.simulation.id = 999998
        self.simulation.storm_id = 1
        self.simulation.dev_scenario_id = 1

        self.patch_simulation_path = mock.patch.object(self.simulation, "path")
        self.mock_simulation_path = self.patch_simulation_path.start()

        self.mock_simulation_path.return_value = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\Test_Cases\Taggart\BaseR011018V4ic\sim\D25yr6h"

        self.model_catalog_dataio = ModelCatalogDbDataIo(self.config)
        self.model_dataio = ModelDataIo(self.config, self.model_catalog_dataio)
        self.model_catalog = ModelCatalog(self.config)
        self.model = Model.initialize_with_current_id(self.config, self.model_catalog_dataio)

        self.model.parent_model_id = 555
        self.model.model_request_id = 777
        self.model.project_phase_id = 1
        self.model.engine_type_id = 1
        self.model.create_date = None
        self.model.deploy_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
        self.model.run_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
        self.model.extract_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
        self.model.created_by = getpass.getuser()
        self.model.model_path = r"\\besfile1\CCSP\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\Test_Cases\Taggart\Final"
        self.model.project_type_id = 1
        self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
        self.model.model_calibration_file = "C:\Temp\Cal"
        self.model.model_status_id = self.config.model_status_id["Working"]
        self.model.model_alteration_file = "C:\Temp\BC"
        self.model.project_num = "E10TEST"
        self.model.create_date = datetime.datetime.today()
        self.model.create_model_alterations_bc([["Stage"]], self.model_catalog_dataio)
        self.model.create_model_alterations_hydrologic([["Area Factor"]], self.model_catalog_dataio)
        self.model.create_model_alterations_hydraulic([["Pipe Roughness"]], self.model_catalog_dataio)
        self.model.create_project_types(["Storm"], self.model_catalog_dataio)
        self.model.create_simulations(self.model_dataio)
        self.model_dataio.set_model_to_read_write(self.model)

    def tearDown(self):
        self.mock_simulation_path = self.patch_simulation_path.stop()

    def test_add_simulation_results(self):
        self.simulation_data_io.append_simulation_results(self.simulation, self.model, self.rrad_db_data_io)

