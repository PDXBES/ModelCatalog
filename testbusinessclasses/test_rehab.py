from unittest import TestCase
from businessclasses.rehab import Rehab
from mock_config import MockConfig
from businessclasses.rehab_result import RehabResult
import datetime
import mock
from dataio.rehab_data_io_new import RehabDataIo
from dataio.rrad_db_data_io import RradDbDataIo

class TestRehab(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.rehab = Rehab(self.config)

        self.rehab.id = 1
        self.rehab.extract_date = datetime.datetime.today()
        self.rehab.last_inspection_date = datetime.datetime.today()
        self.rehab.purpose = "purpose"

        self.rehab_result = RehabResult()
        self.rehab_result.asmrecommendedaction = "SP"
        self.rehab_result.apw = 1
        self.rehab_result.apwspot = 3
        self.rehab_result.bpw = 2
        self.rehab_result.asmrecommendednbcr = 5

        self.patch_copy_rehab_results_to_memory = mock.patch("dataio.rehab_data_io_new.RehabDataIo.copy_rehab_results_to_memory")
        self.mock_copy_rehab_results_to_memory = self.patch_copy_rehab_results_to_memory.start()

        self.rrad_db_data_io = RradDbDataIo(self.config)
        self.rehab_data_io = RehabDataIo(self.config, self.rrad_db_data_io)

        self.patch_create_objects_from_table_with_current_id = mock.patch("dataio.rrad_db_data_io.RradDbDataIo.create_objects_from_table_with_current_id")
        self.mock_create_objects_from_table_with_current_id = self.patch_create_objects_from_table_with_current_id.start()

    def tearDown(self):
        self.mock_copy_rehab_results_to_memory = self.patch_copy_rehab_results_to_memory.stop()
        self.mock_create_objects_from_table_with_current_id = self.patch_create_objects_from_table_with_current_id.stop()


    def test_valid_rehab_has_id_extract_date_last_inspection_date_purpose_returns_true(self):
        is_valid = self.rehab.valid
        self.assertTrue(is_valid)

    def test_valid_rehab_has_invalid_id_returns_false(self):
        self.rehab.id = "one"
        is_valid = self.rehab.valid
        self.assertFalse(is_valid)

    def test_valid_rehab_has_invalid_extract_date_returns_false(self):
        self.rehab.extract_date = "date"
        is_valid = self.rehab.valid
        self.assertFalse(is_valid)

    def test_valid_rehab_has_invalid_last_inspection_date_returns_false(self):
        self.rehab.last_inspection_date = "date"
        is_valid = self.rehab.valid
        self.assertFalse(is_valid)

    def test_valid_rehab_has_invalid_purpose_returns_false(self):
        self.rehab.purpose = None
        is_valid = self.rehab.valid
        self.assertFalse(is_valid)

    def test_create_rehab_results_calls_copy_rehab_results_to_memory_with_correct_arguments(self):
        rehab_results_table_name = "rehab_results_table_name"
        self.rehab.create_rehab_results(self.rehab_data_io)
        self.mock_copy_rehab_results_to_memory.assert_called_with(rehab_results_table_name, self.rehab)

    def test_create_rehab_results_calls_create_objects_from_table_with_current_id_with_correct_arguments(self):
        rehab_results_table_name = "rehab_results_table_name"
        self.rehab.create_rehab_results(self.rehab_data_io)
        self.mock_create_objects_from_table_with_current_id.assert_called_with("rehab_result", rehab_results_table_name, RehabResult.input_field_attribute_lookup())

