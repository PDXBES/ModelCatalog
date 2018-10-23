from unittest import TestCase
import mock
from mock_config import MockConfig
import arcpy
from db_data_io import DbDataIo
from data_io_exception import Field_names_length_does_not_match_row_length_exception
from generic_object import GenericObject
from collections import OrderedDict

class TestDataIO(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.db_data_io = DbDataIo(self.config)
        self.object_class = None
        self.field_names_retrieve_id = ["Object_Type", "Current_ID"]
        self.mock_update_cursor = mock.MagicMock(arcpy.da.UpdateCursor)
        self.mock_insert_cursor = mock.MagicMock(arcpy.da.InsertCursor)
        self.mock_update_cursor.__iter__.return_value = iter([("object_1", 44), ("object_2", 55)])

        self.patch_da_UpdateCursor = mock.patch("arcpy.da.UpdateCursor")
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.start()

        self.patch_da_InsertCursor = mock.patch("arcpy.da.InsertCursor")
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.start()

        self.mock_da_InsertCursor.return_value = self.mock_insert_cursor
        self.mock_generic_object = mock.MagicMock("GenericObject")
        self.mock_generic_object.id = 1
        self.mock_generic_object.name = "name"
        self.mock_generic_object.valid = False

        self.field_attribute_lookup = OrderedDict()
        self.field_attribute_lookup["id_field"] = "id"
        self.field_attribute_lookup["name"] = "name"

        self.object_tracking_sde_path = "object_tracking_sde_path"


    def tearDown(self):
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.stop()
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.stop()


    def test_retrieve_current_id_called_update_cursor(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        self.db_data_io.retrieve_current_id("object_1")
        self.assertTrue(self.mock_da_UpdateCursor.called)

    def test_retrieve_current_id_called_with_correct_arguments(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        self.db_data_io.current_id_database_table_path = "current_id_database_table_path"
        self.db_data_io.retrieve_current_id("object_1")
        self.mock_da_UpdateCursor.assert_called_with("current_id_database_table_path",self.field_names_retrieve_id)

    def test_retrieve_current_id_return_current_ID(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_id = self.db_data_io.retrieve_current_id("object_1")
        self.assertTrue(current_id == 44)

    def test_retrieve_current_id_update_next_id_of_object_1(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        self.db_data_io.retrieve_current_id("object_1")
        self.assertTrue(self.mock_update_cursor.updateRow.called)
        self.mock_update_cursor.updateRow.assert_called_with(["object_1", 45])

    def test_retrieve_current_id_update_next_id_of_object_2(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        self.db_data_io.retrieve_current_id("object_2")
        self.assertTrue(self.mock_update_cursor.updateRow.called)
        self.mock_update_cursor.updateRow.assert_called_with(["object_2", 56])


    def test_add_object_calls_insert_cursor(self):
        self.mock_generic_object.valid = True
        self.db_data_io.add_object(self.mock_generic_object, self.field_attribute_lookup, self.object_tracking_sde_path)
        self.assertTrue(self.mock_da_InsertCursor.called)

    def test_add_object_calls_insert_cursor_insert_row(self):
        self.mock_generic_object.valid = True
        self.db_data_io.add_object(self.mock_generic_object, self.field_attribute_lookup, self.object_tracking_sde_path)
        self.assertTrue(self.mock_insert_cursor.insertRow.called)

    def test_add_object_calls_insertRow_with_correct_arguments(self):
        self.mock_generic_object.valid = True
        self.db_data_io.add_object(self.mock_generic_object, self.field_attribute_lookup, self.object_tracking_sde_path)
        self.mock_insert_cursor.insertRow.assert_called_with([1, "name"])

    def test_create_row_from_object_creates_row_with_correct_values(self):
        row = self.db_data_io.create_row_from_object(self.mock_generic_object, self.field_attribute_lookup)
        self.assertEquals(row, [1, "name"])

    def test_create_row_from_object_raise_exception_when_attribute_name_does_not_exist(self):
        self.field_attribute_lookup["color"] = "red"
        with self.assertRaises(AttributeError):
            self.db_data_io.create_row_from_object(self.mock_generic_object, self.field_attribute_lookup)


