import unittest
import os
from businessclasses.model_catalog import ModelCatalog
from businessclasses.model import Model
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from dataio.model_data_io import ModelDataIo
import getpass
import datetime
import arcpy
from businessclasses.config import Config
from businessclasses.model_catalog_exception import InvalidModelException
from businessclasses.model_catalog_exception import AppendModelAlterationsException
import mock

# This allows a file without a .py extension to be imported (ESRI pyt file)
executable_path = os.path.dirname(os.path.realpath(__file__))
pyt_path = os.path.abspath(os.path.join(executable_path, '..', "ModelCatalog_tools.pyt"))
from imp import load_source
model_catalog_tools = load_source("ModelCatalog_tools", pyt_path)

test_flag = "TEST"
class EmgaatsRegistrationIntegrationTest(unittest.TestCase):
    def setUp(self):

        self.config = Config(test_flag)
        cip_numbers = self.config.unique_cip_numbers
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
        self.model.model_path = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\Test_Cases\Calibration\OAK\Final"
        self.model.project_type_id = 1
        self.model.model_purpose_id = self.config.model_purpose_id["Calibration"]
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
        self.model_dataio.set_model_to_read_write(self.model)


    def test_model_registration_with_model_status_working(self):
        self.model_dataio.create_model_geometry(self.model)
        self.model_catalog.add_model(self.model)
        model_catalog_tools.EMGAATS_Model_Registration_function(self.model_catalog, self.config)
        self.assertFalse(self.model_dataio.check_model_is_read_only(self.model))
        arcpy.AddMessage("\n")

#TODO: Create appropriate models with correct simulation storms

    def test_model_registration_with_model_status_final_model_purpose_calibration_add_model_to_catalog_no_results_to_rrad(self):
        self.model_id = self.model_catalog_dataio.retrieve_current_model_id()
        self.model.model_status_id = self.config.model_status_id["Final"]
        self.model.create_date = datetime.datetime.today()
        self.model_dataio.create_model_geometry(self.model)
        self.model_catalog.add_model(self.model)
        model_catalog_tools.EMGAATS_Model_Registration_function(self.model_catalog, self.config)
        self.assertTrue(self.model_dataio.check_model_is_read_only(self.model))
        arcpy.AddMessage("\n")

    def test_model_registration_with_model_status_final_model_purpose_characterization_add_model_to_catalog_results_to_rrad(self):
        self.model.model_path = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\Test_Cases\Characterization\SunnysideSouth\30pct_Base_Cal"
        self.model_dataio.set_model_to_read_write(self.model)
        self.model.create_simulations(self.model_dataio)
        self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
        self.model_id = self.model_catalog_dataio.retrieve_current_model_id()
        self.model.model_status_id = self.config.model_status_id["Final"]
        self.model_dataio.create_model_geometry(self.model)
        self.model.create_date = datetime.datetime.today()
        self.model_dataio.create_model_geometry(self.model)
        self.model_catalog.add_model(self.model)
        model_catalog_tools.EMGAATS_Model_Registration_function(self.model_catalog, self.config)
        self.assertTrue(self.model_dataio.check_model_is_read_only(self.model))
        arcpy.AddMessage("\n")

    def test_model_registration_with_model_invalid(self):
        self.model.model_path = r"Invalid_path"
        self.model_id = self.model_catalog_dataio.retrieve_current_model_id()
        self.model.create_date = datetime.datetime.today()
        try:
            self.model_dataio.create_model_geometry(self.model)
            self.model_catalog.add_model(self.model)
            model_catalog_tools.EMGAATS_Model_Registration_function(self.model_catalog, self.config)

        except InvalidModelException:
            self.model.model_valid_diagnostic()
            arcpy.AddError("Model is not valid")
        arcpy.AddMessage("\n")

    def test_model_registration_with_model_status_working_exception_thrown_after_model_added_to_db_should_rollback(self):
        #TODO - AppendModelAlterationsException does not seem to be raised to the pyt ExcecuteError (395)
        # The test needs to be reworked to deal with this
        with mock.patch("dataio.model_data_io.ModelDataIo.append_simulations") as mock_add_simulations:
            self.model.id = 999
            mock_add_simulations.side_effect = Exception()
            self.model_dataio.create_model_geometry(self.model)
            self.model_catalog.add_model(self.model)
            with self.assertRaises(AppendModelAlterationsException):
                model_catalog_tools.EMGAATS_Model_Registration_function(self.model_catalog, self.config)
        arcpy.AddMessage("\n")

#TODO: Add test for model without alterations
