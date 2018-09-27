from unittest import TestCase
import mock
import arcpy
from data_io import DataIO

class TestDataIO(TestCase):

    def setUp(self):

        self.dataio = DataIO()
        self.field_names_retrieve_id = ["Object_Type", "Current_ID"]
        self.mock_update_cursor = mock.MagicMock(arcpy.da.UpdateCursor)
        self.mock_update_cursor.__iter__.return_value = iter([("object_1", 44), ("object_2", 55)])

        self.patch_da_UpdateCursor = mock.patch("arcpy.da.UpdateCursor")
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.start()

    def tearDown(self):
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.stop()


    def test_retrieve_current_id_called_update_cursor(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        self.dataio.retrieve_current_id("object_1")
        self.assertTrue(self.mock_da_UpdateCursor.called)

    def test_retrieve_current_id_called_with_correct_arguments(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        self.dataio.current_id_database_table_path = "current_id_database_table_path"
        self.dataio.retrieve_current_id("object_1")
        self.mock_da_UpdateCursor.assert_called_with("current_id_database_table_path",self.field_names_retrieve_id)

    def test_retrieve_current_id_return_current_ID(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_id = self.dataio.retrieve_current_id("object_1")
        self.assertTrue(current_id == 44)

    def test_retrieve_current_id_update_next_id_of_object_1(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        self.dataio.retrieve_current_id("object_1")
        self.assertTrue(self.mock_update_cursor.updateRow.called)
        self.mock_update_cursor.updateRow.assert_called_with(["object_1", 45])

    def test_retrieve_current_id_update_next_id_of_object_2(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        self.dataio.retrieve_current_id("object_2")
        self.assertTrue(self.mock_update_cursor.updateRow.called)
        self.mock_update_cursor.updateRow.assert_called_with(["object_2", 56])
