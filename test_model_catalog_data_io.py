from unittest import TestCase
from model_catalog_data_io import ModelCatalogDataIO
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
        "Model_Purpose_ID",
        "Model_Calibration_file",
        "Model_Status_ID",
        "Model_Alteration_file",
        "Project_Num"]
        self.field_names_retrieve_id = ["Object_Type", "Current_ID"]
        self.mock_update_cursor = mock.MagicMock(arcpy.da.UpdateCursor)
        self.mock_update_cursor.__iter__.return_value = iter([("model", 44), ("simulation", 55)])
        test = self.mock_update_cursor.next()
        self.model_catalog.models = []
        self.model_catalog.models.append(self.model)
        self.model.valid = True

        self.patch_da_UpdateCursor = mock.patch("arcpy.da.UpdateCursor")
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.start()

    def tearDown(self):
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.stop()


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
                                                  None, None, None, None, None, None])

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

    def test_retrieve_current_model_id(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_model_id = self.modelcatalogdataio.retrieve_current_model_id()
        self.assertTrue(current_model_id == 44)

    def test_retrieve_current_simulation_id(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_simulation_id = self.modelcatalogdataio.retrieve_current_simulation_id()
        self.assertTrue(current_simulation_id == 55)



