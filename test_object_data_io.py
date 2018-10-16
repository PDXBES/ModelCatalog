from unittest import TestCase
import mock
from mock_config import MockConfig
import arcpy
from object_data_io import ObjectDataIo
from data_io_exception import Field_names_length_does_not_match_row_length_exception
from generic_object import GenericObject
from collections import OrderedDict


class TestObjectDataIo(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.parent_id = 1

        self.object_data_io = ObjectDataIo(self.config)
        self.object_class = None
        self.field_names_retrieve_id = ["Object_Type", "Current_ID"]



        self.patch_da_InsertCursor = mock.patch("arcpy.da.InsertCursor")
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.start()

        self.mock_generic_object = mock.MagicMock("GenericObject")
        self.mock_generic_object.id = 1
        self.mock_generic_object.name = "name"
        self.mock_generic_object.valid = False

        self.field_attribute_lookup = OrderedDict()
        self.field_attribute_lookup["id_field"] = "id"
        self.field_attribute_lookup["name"] = "name"

        self.object_tracking_sde_path = "object_tracking_sde_path"


    def tearDown(self):
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.stop()


    def test_add_object_calls_insert_cursor(self):
        self.mock_generic_object.valid = True
        self.object_data_io.add_object(self.parent_id, self.mock_generic_object, self.field_attribute_lookup, self.object_tracking_sde_path)
        self.assertTrue(self.mock_da_InsertCursor.called)

    def test_add_object_calls_insert_cursor_with_correct_arguments(self):
        self.object_data_io.add_object(self.parent_id, self.mock_generic_object, self.field_attribute_lookup, self.object_tracking_sde_path)
        #TODO:
