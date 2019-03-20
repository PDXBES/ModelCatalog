from unittest import TestCase
import os
import ctypes
from ctypes import wintypes
import mock
from businessclasses.model_catalog_exception import InvalidModelPathException
from dataio.utility import Utility
from testbusinessclasses.mock_config import MockConfig
from stat import S_IREAD, S_IRGRP, S_IROTH

class TestUtility(TestCase):


    def setUp(self):
        self.utility = Utility()
        self.patch_convert_mapped_letter_drive_to_unc_path = mock.patch.object(self.utility, "convert_mapped_letter_drive_to_unc_path")
        self.mock_convert_mapped_letter_drive_to_unc_path = self.patch_convert_mapped_letter_drive_to_unc_path.start()

    def tearDown(self):
        self.mock_convert_mapped_letter_drive_to_unc_path = self.patch_convert_mapped_letter_drive_to_unc_path.stop()


    def test_check_path_has_mapped_network_drive_calls_convert_mapped_letter_drive_to_unc_path_called_with_correct_arguments(self):
        mock_path = r"V:\test\test"
        self.utility.check_path(mock_path)
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




