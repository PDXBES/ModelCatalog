from unittest import TestCase
import mock
from testbusinessclasses.mock_config import MockConfig
import arcpy
from dataio.rrad_data_io import RradDbDataIo
from businessclasses.rehab import Rehab
from businessclasses.generic_class_factory import GenericClassFactory

class TestRradDataIO(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.mock_rehab = mock.MagicMock(Rehab)
        generic_class_factory = GenericClassFactory(self.config)

        self.rrad_data_io = RradDbDataIo(self.config)
        self.field_names_retrieve_id = ["Object_Type", "Current_ID"]
        self.mock_update_cursor = mock.MagicMock(arcpy.da.UpdateCursor)
        self.mock_update_cursor.__iter__.return_value = iter([("rehab", 44), ("object_2", 55)])

        self.patch_da_UpdateCursor = mock.patch("arcpy.da.UpdateCursor")
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.start()

    def tearDown(self):
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.stop()

    def test_retrieve_current_rehab_id(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_model_id = self.rrad_data_io.retrieve_current_rehab_id()
        self.assertTrue(current_model_id == 44)

    def test_add_rehab_calls_add_object(self):
        with mock.patch.object(self.rrad_data_io, "append_object_to_db") as mock_append_object_to_db:
            self.rrad_data_io.add_rehab(self.mock_rehab)
            self.assertTrue(mock_append_object_to_db.called)
