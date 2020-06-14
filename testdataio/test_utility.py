from unittest import TestCase
import os
import arcpy
import ctypes
from ctypes import wintypes
import mock
from businessclasses.config import Config
from businessclasses.model_catalog_exception import InvalidModelPathException
from dataio.utility import Utility
from testbusinessclasses.mock_config import MockConfig
from stat import S_IREAD, S_IRGRP, S_IROTH
import datetime

class TestUtility(TestCase):


    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.utility = Utility(self.config)

        self.patch_convert_mapped_letter_drive_to_unc_path = mock.patch("dataio.utility.Utility.convert_mapped_letter_drive_to_unc_path")
        self.mock_convert_mapped_letter_drive_to_unc_path = self.patch_convert_mapped_letter_drive_to_unc_path.start()

        self.patch_DeleteRows_management = mock.patch("arcpy.DeleteRows_management")
        self.mock_DeleteRows_management = self.patch_DeleteRows_management.start()

        self.patch_TruncateTable_management = mock.patch("arcpy.TruncateTable_management")
        self.mock_TruncateTable_management = self.patch_TruncateTable_management.start()

    def tearDown(self):
        self.mock_convert_mapped_letter_drive_to_unc_path = self.patch_convert_mapped_letter_drive_to_unc_path.stop()
        self.mock_DeleteRows_management = self.patch_DeleteRows_management.stop()
        self.mock_TruncateTable_management = self.patch_TruncateTable_management.stop()

    def test_check_path_has_mapped_network_drive_calls_convert_mapped_letter_drive_to_unc_path_called_with_correct_arguments(self):
        mock_path = r"V:\test\test"
        Utility.check_path(mock_path)
        self.mock_convert_mapped_letter_drive_to_unc_path.assert_called_with("V:")

    def test_check_path_has_mapped_network_drive_calls_convert_mapped_letter_drive_to_unc_path_returns_correct_path(self):
        mock_path = r"V:\test\test"
        self.mock_convert_mapped_letter_drive_to_unc_path.return_value = r"\\besfile1"
        return_path = self.utility.check_path(mock_path)
        self.assertEqual(return_path, r"\\besfile1\test\test")

    def test_check_path_is_unc_path_returns_correct_path(self):
        mock_path = r"\\besfile1\test\test"
        return_path = self.utility.check_path(mock_path)
        self.assertEqual(return_path, r"\\besfile1\test\test")

    def test_check_path_raise_exception_when_winError_throws_exception(self):
        mock_path = r"V:\test\test"
        self.mock_convert_mapped_letter_drive_to_unc_path.side_effect = Exception
        with self.assertRaises(Exception):
            self.utility.check_path(mock_path)

    def test_model_catalog_test_data_cleanup_calls_truncate_table_with_correct_arguments(self):
        self.utility.model_catalog_test_data_cleanup()
        feature_class_list = ["model_tracking_sde_path", "model_alt_bc_sde_path",
                                  "model_alt_hydraulic_sde_path", "model_alt_hydrologic_sde_path",
                                  "project_type_sde_path", "simulation_sde_path",
                                  "geometry_nodes_sde_path", "geometry_areas_sde_path",
                                  "geometry_links_sde_path",
                                  "results_area_sde_path", "results_link_sde_path",
                                  "results_node_sde_path", "results_node_flooding_sde_path", "storage_sde_path"]
        self.assertTrue(self.mock_TruncateTable_management.called)
        for counter, argument in enumerate(self.mock_TruncateTable_management.call_args_list):
            feature_class = argument[0][0]
            self.assertEquals(feature_class, feature_class_list[counter])

    def test_format_date_string_calls_strftime_with_correct_date_string_argument(self):
        date = mock.MagicMock(datetime.date)
        date.strftime.return_value = "date string"
        return_string = Utility.format_date(date)
        self.assertEquals(return_string, "date string")
        self.assertEquals("%m/%d/%Y %H:%M %p", date.strftime.call_args[0][0])

    #TODO: test for test flags in test data cleanup

    #TODO: test for deleterows if truncate throws exception in test data cleanup

