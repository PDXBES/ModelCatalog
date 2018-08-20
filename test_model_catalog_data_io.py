from unittest import TestCase
from model_catalog_data_io import ModelCatalogDataIO
import mock
from model_catalog import ModelCatalog
from model import Model
import arcpy
from model_catalog_exception import ModelCatalog_exception, Field_names_length_does_not_match_row_length_exception
from config import Config

class TestModelCatalogDataIO(TestCase):
    def setUp(self):
        self.config = mock.MagicMock(Config)
        self.config.current_id_table_sde_path = "current_id_table_sde_path"
        self.config.model_tracking_sde_path = "model_tracking_sde_path"
        self.modelcatalogdataio = ModelCatalogDataIO(self.config)
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
        self.model.model_alterations_id = None
        self.model.model_alteration_file = None
        self.model.project_num = None

        self.database_location = "location"
        self.field_names = ["Model_ID",
        "Parent_Model_ID",
        "Model_Request_ID",
        "Project_Phase_ID",
        "Engine_Type_ID",
        "Create_Date",
        "Created_by",
        "Deploy_Date",
        "Extract_Date",
        "Run_Date",
        "Model_Path",
        "Project_Type_ID",
        "Model_Purpose_ID",
        "Model_Calibration_file",
        "Model_Status_ID",
        "Model_Alterations_ID",
        "Model_Alteration_file",
        "Project_Num"]
        self.field_names_retrieve_id = ["Object_Type", "Current_ID"]
        self.mock_update_cursor = mock.MagicMock(arcpy.da.UpdateCursor)
        self.mock_update_cursor.__iter__.return_value = iter([("model", 44), ("simulation", 55)])
        test = self.mock_update_cursor.next()
        self.model_catalog.models = []
        self.model_catalog.models.append(self.model)
        self.model.valid = True


    @mock.patch("arcpy.da.InsertCursor")
    def test_add_model_called_insert_cursor(self, mock_da_InsertCursor):
        self.modelcatalogdataio.add_model(self.model_catalog.models[0], self.field_names)
        self.assertTrue(mock_da_InsertCursor.called)

    @mock.patch("arcpy.da.InsertCursor")
    def test_add_model_called_with_correct_arguments(self, mock_da_InsertCursor):
        self.modelcatalogdataio.add_model(self.model_catalog.models[0], self.field_names)
        mock_da_InsertCursor.assert_called_with(self.config.model_tracking_sde_path, self.field_names)

    def test_add_model_model_parameters_are_passed_into_row(self):
        mock_cursor = mock.MagicMock(arcpy.da.InsertCursor)
        with mock.patch("arcpy.da.InsertCursor") as mock_da_InsertCursor:
            mock_da_InsertCursor.return_value = mock_cursor
            self.modelcatalogdataio.add_model(self.model_catalog.models[0], self.field_names)
        self.assertTrue(mock_cursor.insertRow.called)
        mock_cursor.insertRow.assert_called_with([0, 0, 0, None, None, None, None, None, None, None,
                                                  None, None, None, None, None, None, None, None])

    @mock.patch("arcpy.da.InsertCursor")
    def test_add_model_add_invalid_model_exception_raised(self, mock_da_InsertCursor):
        self.model.valid = False
        with self.assertRaises(ModelCatalog_exception):
            self.modelcatalogdataio.add_model(self.model_catalog.models[0], self.field_names)

    @mock.patch("arcpy.da.InsertCursor")
    def test_add_model_field_names_length_does_not_equal_row_length_exception_raised(self, mock_da_InsertCursor):
        self.field_names.append("asdf")
        with self.assertRaises(Field_names_length_does_not_match_row_length_exception):
            self.modelcatalogdataio.add_model(self.model_catalog.models[0], self.field_names)

    def test_retrieve_current_id_called_update_cursor(self):
        with mock.patch("arcpy.da.UpdateCursor") as mock_da_UpdateCursor:
            mock_da_UpdateCursor.return_value = self.mock_update_cursor
            self.modelcatalogdataio.retrieve_current_id("model")
        self.assertTrue(mock_da_UpdateCursor.called)

    def test_retrieve_current_id_called_with_correct_arguments(self):
        with mock.patch("arcpy.da.UpdateCursor") as mock_da_UpdateCursor:
            mock_da_UpdateCursor.return_value = self.mock_update_cursor
            self.modelcatalogdataio.retrieve_current_id("model")
        mock_da_UpdateCursor.assert_called_with(self.config.current_id_table_sde_path, self.field_names_retrieve_id)

    def test_retrieve_current_id_update_next_id_of_model_object(self):
        with mock.patch("arcpy.da.UpdateCursor") as mock_da_UpdateCursor:
            mock_da_UpdateCursor.return_value = self.mock_update_cursor
            self.modelcatalogdataio.retrieve_current_id("model")
        self.assertTrue(self.mock_update_cursor.updateRow.called)
        self.mock_update_cursor.updateRow.assert_called_with(["model", 45])

    def test_retrieve_current_id_update_next_id_of_simulation_object(self):
        with mock.patch("arcpy.da.UpdateCursor") as mock_da_UpdateCursor:
            mock_da_UpdateCursor.return_value = self.mock_update_cursor
            self.modelcatalogdataio.retrieve_current_id("simulation")
        self.assertTrue(self.mock_update_cursor.updateRow.called)
        self.mock_update_cursor.updateRow.assert_called_with(["simulation", 56])

    def test_retrieve_current_id_return_current_ID(self):
        with mock.patch("arcpy.da.UpdateCursor") as mock_da_UpdateCursor:
            mock_da_UpdateCursor.return_value = self.mock_update_cursor
            current_id = self.modelcatalogdataio.retrieve_current_id("model")
        self.assertTrue(current_id == 44)

    def test_retrieve_current_model_id(self):
        with mock.patch("arcpy.da.UpdateCursor") as mock_da_UpdateCursor:
            mock_da_UpdateCursor.return_value = self.mock_update_cursor
            current_model_id = self.modelcatalogdataio.retrieve_current_model_id()
        self.assertTrue(current_model_id == 44)

    def test_retrieve_current_simulation_id(self):
        with mock.patch("arcpy.da.UpdateCursor") as mock_da_UpdateCursor:
            mock_da_UpdateCursor.return_value = self.mock_update_cursor
            current_simulation_id = self.modelcatalogdataio.retrieve_current_simulation_id()
        self.assertTrue(current_simulation_id == 55)



