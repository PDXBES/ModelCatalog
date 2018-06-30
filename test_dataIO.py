from unittest import TestCase
from dataIO import DataIO
import mock
from modelCatalog import ModelCatalog
from Model import Model
import arcpy


class TestDataIO(TestCase):
    def setUp(self):
        self.dataio = DataIO()
        self.model_catalog = mock.MagicMock(ModelCatalog)
        self.model = mock.MagicMock(Model)
        self.model.Parent_Model_ID = 111
        self.model.Model_Request_ID = 222
        self.database_location = "location"
        self.field_names = ["test"]
        self.model_catalog.models = []
        self.model_catalog.models.append(self.model)

    @mock.patch("arcpy.da.UpdateCursor")
    def test_add_model_called_update_cursor(self, mock_da_UpdateCursor):
        self.dataio.add_model(self.model_catalog.models[0], self.database_location, self.field_names)
        self.assertTrue(mock_da_UpdateCursor.called)

    @mock.patch("arcpy.da.UpdateCursor")
    def test_add_model_called_with_correct_arguments(self, mock_da_UpdateCursor):
        self.dataio.add_model(self.model_catalog.models[0], self.database_location, self.field_names)
        mock_da_UpdateCursor.assert_called_with("location", ["test"])

    def test_add_model_model_parameters_are_passed_into_row(self):
        mock_cursor = mock.MagicMock(arcpy.da.UpdateCursor)
        with mock.patch("arcpy.da.UpdateCursor") as mock_da_UpdateCursor:
            mock_da_UpdateCursor.return_value = mock_cursor
            self.dataio.add_model(self.model_catalog.models[0], self.database_location, self.field_names)
        self.assertTrue(mock_cursor.updateRow.called)
        mock_cursor.updateRow.assert_called_with([111, 222])

    def test_insert_model_model_parameters_are_passed_into_row(self):
        mock_cursor = mock.MagicMock(arcpy.da.InsertCursor)
        with mock.patch("arcpy.da.InsertCursor") as mock_da_InsertCursor:
            mock_da_InsertCursor.return_value = mock_cursor
            self.dataio.insert_model(self.model_catalog.models[0], self.database_location, self.field_names)
        self.assertTrue(mock_cursor.insertRow.called)
        mock_cursor.insertRow.assert_called_with([111, 222])

    # Test doesn't work (The patch decorator gets rid of the spec for the mock cursor?)
    @mock.patch("arcpy.da.UpdateCursor")
    def test_add_model_model1_parameters_are_passed_into_row(self, mock_da_UpdateCursor):
        mock_cursor = mock.MagicMock(arcpy.da.UpdateCursor)
        mock_da_UpdateCursor.return_value = mock_cursor
        self.dataio.add_model(self.model_catalog.models[0], self.database_location, self.field_names)
        self.assertTrue(mock_cursor.updateRow.called)
        mock_cursor.updateRow.assert_called_with([111, 222])

    # Test doesn't work (Seems to be an issue with the with and as in the method?)
    def test_insert_model_model1_parameters_are_passed_into_row(self):
        mock_cursor = mock.MagicMock(arcpy.da.InsertCursor)
        with mock.patch("arcpy.da.InsertCursor") as mock_da_InsertCursor:
            mock_da_InsertCursor.return_value = mock_cursor
            self.dataio.insert_model1(self.model_catalog.models[0], self.database_location, self.field_names)
        self.assertTrue(mock_cursor.insertRow.called)
        mock_cursor.insertRow.assert_called_with([111, 222])
