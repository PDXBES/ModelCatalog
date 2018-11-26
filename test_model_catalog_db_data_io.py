from unittest import TestCase
from model_catalog_db_data_io import ModelCatalogDbDataIo
import mock
from model_catalog import ModelCatalog
from model import Model
import arcpy
from model_catalog_exception import ModelCatalog_exception, Field_names_length_does_not_match_row_length_exception
from mock_config import MockConfig
from model_data_io import ModelDataIo

class TestModelCatalogDbDataIO(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.modelcatalogdataio = ModelCatalogDbDataIo(self.config)
        self.model_catalog = mock.MagicMock(ModelCatalog)
        self.model = mock.MagicMock(Model)
        self.model_data_io = ModelDataIo(self.config, self.modelcatalogdataio)
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
        self.mock_Editor = mock.MagicMock("arcpy.da.Editor")

        self.mock_update_cursor = mock.MagicMock(arcpy.da.UpdateCursor)
        self.mock_update_cursor.__iter__.return_value = iter([("model", 44), ("simulation", 55), ("model_alteration", 66)])
        self.patch_da_UpdateCursor = mock.patch("arcpy.da.UpdateCursor")
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.start()

        self.patch_da_InsertCursor = mock.patch("arcpy.da.InsertCursor")
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.start()

        self.patch_add_object = mock.patch.object(self.modelcatalogdataio, "add_object")
        self.mock_add_object = self.patch_add_object.start()

        self.patch_read_simulations = mock.patch("model_data_io.ModelDataIo.read_simulations")
        self.mock_read_simulations = self.patch_read_simulations.start()

        self.patch_add_simulations = mock.patch("model_data_io.ModelDataIo.add_simulations")
        self.mock_add_simulations = self.patch_add_simulations.start()

        self.patch_add_model_alterations = mock.patch("model_data_io.ModelDataIo.add_model_alterations")
        self.mock_add_model_alterations = self.patch_add_model_alterations.start()

        self.patch_add_project_types = mock.patch("model_data_io.ModelDataIo.add_project_types")
        self.mock_add_project_types = self.patch_add_project_types.start()

        self.patch_da_Editor = mock.patch("arcpy.da.Editor")
        self.mock_da_Editor = self.patch_da_Editor.start()
        self.mock_da_Editor.return_value = self.mock_Editor

        self.patch_startEditing = mock.patch("arcpy.da.Editor.startEditing")
        self.mock_startEditing = self.patch_startEditing.start()

        self.patch_startOperation = mock.patch("arcpy.da.Editor.startOperation")
        self.mock_startOperation = self.patch_startOperation.start()

        self.patch_stopOperation = mock.patch("arcpy.da.Editor.stopOperation")
        self.mock_stopOperation = self.patch_stopOperation.start()

        self.patch_stopEditing = mock.patch("arcpy.da.Editor.stopEditing")
        self.mock_stopEditing = self.patch_stopEditing.start()

    def tearDown(self):
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.stop()
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.stop()
        self.mock_add_object = self.patch_add_object.stop()
        self.mock_read_simulations = self.patch_read_simulations.stop()
        self.mock_add_simulations = self.patch_add_simulations.stop()
        self.mock_add_model_alterations = self.patch_add_model_alterations.stop()
        self.mock_add_project_types = self.patch_add_project_types.stop()
        self.mock_da_Editor = self.patch_da_Editor.stop()
        self.mock_startEditing = self.patch_startEditing.stop()
        self.mock_startOperation = self.patch_startOperation.stop()
        self.mock_stopOperation = self.patch_stopOperation.stop()
        self.mock_stopEditing = self.patch_stopEditing.stop()

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
        self.modelcatalogdataio.add_model(self.model, self.model_data_io)
        self.assertTrue(self.mock_add_object.called)

    def test_add_model_calls_read_simulations(self):
        self.modelcatalogdataio.add_model(self.model, self.model_data_io)
        self.assertTrue(self.mock_read_simulations.called)

    def test_add_model_calls_add_simulations(self):
        self.modelcatalogdataio.add_model(self.model, self.model_data_io)
        self.assertTrue(self.mock_add_simulations.called)

    def test_add_model_calls_add_model_alterations(self):
        self.modelcatalogdataio.add_model(self.model, self.model_data_io)
        self.assertTrue(self.mock_add_model_alterations.called)

    def test_add_model_calls_add_project_types(self):
        self.modelcatalogdataio.add_model(self.model, self.model_data_io)
        self.assertTrue(self.mock_add_project_types.called)

    #TODO - write tests for add model method internals






