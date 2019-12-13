from unittest import TestCase
import mock
from testbusinessclasses.mock_config import MockConfig
import arcpy
from dataio.rrad_db_data_io import RradDbDataIo
from dataio.rehab_data_io import RehabDataIo
from businessclasses.rehab import Rehab

class TestRradDataIO(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.mock_rehab = mock.MagicMock(Rehab)

        self.rrad_db_data_io = RradDbDataIo(self.config)

        #self.rehab_data_io = RehabDataIo(self.config, self.rrad_db_data_io)

        self.field_names_retrieve_id = ["Object_Type", "Current_ID"]
        self.mock_update_cursor = mock.MagicMock(arcpy.da.UpdateCursor)
        self.mock_update_cursor.__iter__.return_value = iter([("Rehab", 44), ("object_2", 55)])

        self.patch_append_object_to_db = mock.patch("dataio.rrad_db_data_io.RradDbDataIo.append_object_to_db")
        self.mock_append_object_to_db = self.patch_append_object_to_db.start()

        self.patch_da_UpdateCursor = mock.patch("arcpy.da.UpdateCursor")
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.start()

        self.patch_create_rehab_results = mock.patch("businessclasses.rehab.Rehab.create_rehab_results")
        self.mock_create_rehab_results = self.patch_create_rehab_results.start()

        self.mock_rehab_data_io = mock.MagicMock(RehabDataIo)




    def tearDown(self):
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.stop()
        self.mock_append_object_to_db = self.patch_append_object_to_db.stop()
        self.mock_create_rehab_result = self.patch_create_rehab_results.start()

    def test_retrieve_current_rehab_id(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_rehab_id = self.rrad_db_data_io.retrieve_current_rehab_id()
        self.assertTrue(current_rehab_id == 44)

    def test_add_rehab_calls_append_object_with_correct_arguments(self):
        self.rrad_db_data_io.add_rehab(self.mock_rehab, self.mock_rehab_data_io)
        self.mock_append_object_to_db.assert_called_with(self.mock_rehab, Rehab.input_field_attribute_lookup(), self.config.rehab_tracking_sde_path,
                                                        self.config.rehab_tracking_sde_path)

    def test_add_rehab_calls_create_rehab_result_with_correct_arguments(self):
        self.rrad_db_data_io.add_rehab(self.mock_rehab, self.mock_rehab_data_io)
        self.mock_rehab.create_rehab_results.assert_called_with(self.mock_rehab_data_io)

    def test_add_rehab_calls_start_editing_session_with_correct_arguments(self):
        self.rrad_db_data_io.add_rehab(self.mock_rehab, self.mock_rehab_data_io)
        self.mock_rehab_data_io.start_editing_session.assert_called_with(self.config.RRAD_sde_path)

    def test_add_rehab_calls_stop_editing_session_no_exceptions_with_correct_arguments(self):
        editor = "editor"
        self.mock_rehab_data_io.start_editing_session.return_value = editor
        self.rrad_db_data_io.add_rehab(self.mock_rehab, self.mock_rehab_data_io)
        self.mock_rehab_data_io.stop_editing_session.assert_called_with(editor, True)

    def test_add_rehab_calls_stop_editing_session_with_exceptions_with_correct_arguments(self):
        editor = "editor"
        self.mock_rehab_data_io.start_editing_session.return_value = editor
        self.mock_append_object_to_db.side_effect = Exception
        self.rrad_db_data_io.add_rehab(self.mock_rehab, self.mock_rehab_data_io)
        self.mock_rehab_data_io.stop_editing_session.assert_called_with(editor, False)

    def test_add_rehab_calls_append_rehab_results_with_correct_arguments(self):
        self.rrad_db_data_io.add_rehab(self.mock_rehab, self.mock_rehab_data_io)
        self.mock_rehab_data_io.append_rehab_results.assert_called_with(self.mock_rehab)

