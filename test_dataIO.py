from unittest import TestCase
from dataIO import DataIO
import mock
from ModelCatalog import ModelCatalog
from Model import Model
import arcpy
from modelCatalog_exception import ModelCatalog_exception, Field_names_length_does_not_match_row_length_exception


class TestDataIO(TestCase):
    def setUp(self):
        self.dataio = DataIO()
        self.model_catalog = mock.MagicMock(ModelCatalog)
        self.model = mock.MagicMock(Model)
        self.model.Parent_Model_ID = 111
        self.model.Model_Request_ID = 222
        self.database_location = "location"
        self.field_names = ["test1", "test2"]
        self.model_catalog.models = []
        self.model_catalog.models.append(self.model)
        self.model.valid = True

    @mock.patch("arcpy.da.InsertCursor")
    def test_add_model_called_update_cursor(self, mock_da_InsertCursor):
        self.dataio.add_model(self.model_catalog.models[0], self.database_location, self.field_names)
        self.assertTrue(mock_da_InsertCursor.called)

    @mock.patch("arcpy.da.InsertCursor")
    def test_add_model_called_with_correct_arguments(self, mock_da_InsertCursor):
        self.dataio.add_model(self.model_catalog.models[0], self.database_location, self.field_names)
        mock_da_InsertCursor.assert_called_with("location", ["test1", "test2"])

    def test_add_model_model_parameters_are_passed_into_row(self):
        mock_cursor = mock.MagicMock(arcpy.da.InsertCursor)
        with mock.patch("arcpy.da.InsertCursor") as mock_da_InsertCursor:
            mock_da_InsertCursor.return_value = mock_cursor
            self.dataio.add_model(self.model_catalog.models[0], self.database_location, self.field_names)
        self.assertTrue(mock_cursor.insertRow.called)
        mock_cursor.insertRow.assert_called_with([111, 222])

    @mock.patch("arcpy.da.InsertCursor")
    def test_add_model_add_invalid_model_exception_raised(self, mock_da_InsertCursor):
        self.model.valid = False
        with self.assertRaises(ModelCatalog_exception):
            self.dataio.add_model(self.model_catalog.models[0], self.database_location, self.field_names)

    @mock.patch("arcpy.da.InsertCursor")
    def test_add_model_field_names_length_does_not_equal_row_length_exception_raised(self, mock_da_InsertCursor):
        self.field_names.append("asdf")
        with self.assertRaises(Field_names_length_does_not_match_row_length_exception):
            self.dataio.add_model(self.model_catalog.models[0], self.database_location, self.field_names)