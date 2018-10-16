from unittest import TestCase
from model_catalog_data_io import ModelCatalogDbDataIo
import mock
from model_catalog import ModelCatalog
from model import Model
import arcpy
from model_catalog_exception import ModelCatalog_exception, Field_names_length_does_not_match_row_length_exception
from mock_config import MockConfig

class TestModelCatalogDataIO(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.modelcatalogdataio = ModelCatalogDbDataIo(self.config)
        self.model_catalog = mock.MagicMock(ModelCatalog)
        self.model = mock.MagicMock(Model)
        self.model.model_id = 0
        self.model.parent_model_id = 0
        self.model.model_request_id = 0
        self.model.project_phase_id = None
        self.model.engine_type_id = None
        self.model.create_date = None
        self.model.deploy_date = None
        self.model.run_date = None
        self.model.extract_date = None
        self.model.created_by = None
        self.model.model_path = None
        self.model.project_type_id = None
        self.model.model_purpose_id = None
        self.model.model_calibration_file = None
        self.model.model_status_id = None
        self.model.model_alteration_file = None
        self.model.project_num = None
        self.model.model_geometry = None

        self.mock_update_cursor = mock.MagicMock(arcpy.da.UpdateCursor)
        self.mock_update_cursor.__iter__.return_value = iter([("model", 44), ("simulation", 55), ("model_alteration", 66)])
        self.patch_da_UpdateCursor = mock.patch("arcpy.da.UpdateCursor")
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.start()

        self.patch_da_InsertCursor = mock.patch("arcpy.da.InsertCursor")
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.start()



    def tearDown(self):
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.stop()
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.stop()


    def test_retrieve_current_model_id(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_model_id = self.modelcatalogdataio.retrieve_current_model_id()
        self.assertTrue(current_model_id == 44)

    def test_retrieve_current_simulation_id(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_simulation_id = self.modelcatalogdataio.retrieve_current_simulation_id()
        self.assertTrue(current_simulation_id == 55)

    def test_retrieve_current_model_alteration_id(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_model_alteration_id = self.modelcatalogdataio.retrieve_current_model_alteration_id()
        self.assertTrue(current_model_alteration_id == 66)

    def test_add_model_calls_add_object(self):
        with mock.patch.object(self.modelcatalogdataio, "add_object") as mock_add_object:
            self.modelcatalogdataio.add_model(self.model)
            self.assertTrue(mock_add_object.called)



