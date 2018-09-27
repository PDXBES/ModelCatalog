from unittest import TestCase
import mock
from mock_config import MockConfig
import arcpy
from rrad_data_io import RradDataIO

class TestRradDataIO(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.rrad_data_io = RradDataIO(self.config)
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
