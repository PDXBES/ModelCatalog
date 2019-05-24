from unittest import TestCase
from dataio.rehab_data_io_new import RehabDataIo

import mock
from testbusinessclasses.mock_config import MockConfig
from businessclasses.rehab import Rehab
import arcpy
from businessclasses.rehab_result import RehabResult
from dataio.rrad_db_data_io import RradDbDataIo


class TestRehabDataIONew(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.rrad_db_data_io = RradDbDataIo(self.config)
        self.rehab_data_io = RehabDataIo(self.config, self.rrad_db_data_io)

        self.patch_make_query_table = mock.patch("arcpy.MakeQueryTable_management")
        self.mock_make_query_table_management = self.patch_make_query_table.start()

    def tearDown(self):
        self.mock_make_query_table_management = self.patch_make_query_table.stop()

    def test_copy_rehab_results_from_nbcr_data_to_memory_calls_make_query_table_management_with_correct_arguments(self):
        input_table = "rehab_nbcr_data_sde_path"
        in_memory_table = "in_memory\\output_table_name"
        output_table_name = "output_table_name"
        fields = RehabResult.nbcr_data_field_attribute_lookup().keys()
        where_clause = "hservstat not in ( 'ABAN' , 'TBAB' , 'DNE' )" + " and " + "cutno = 0 and compkey is not Null"
        self.rehab_data_io.copy_rehab_results_from_nbcr_data_to_memory(output_table_name)
        self.mock_make_query_table_management.assert_called_with(input_table, in_memory_table, "", "", fields, where_clause)

    def test_copy_rehab_results_from_rehab_branches_to_memory_calls_make_query_table_with_correct_arguments(self):
        input_table = "rehab_branches_sde_path"
        in_memory_table = "in_memory\\output_table_name"
        output_table_name = "output_table_name"
        fields = RehabResult.rehab_branches_field_attribute_lookup().keys()
        self.rehab_data_io.copy_rehab_results_from_rehab_branches_to_memory(output_table_name)
        self.mock_make_query_table_management.assert_called_with(input_table, in_memory_table, "", "", fields, "")

    def test_copy_rehab_results_from_tv_ratings_to_memory_calls_make_query_table_with_correct_arguments(self):
        input_table = "tv_ratings_sde_path"
        in_memory_table = "in_memory\\output_table_name"
        output_table_name = "output_table_name"
        fields = RehabResult.tv_ratings_field_attribute_lookup().keys()
        self.rehab_data_io.copy_rehab_results_from_tv_ratings_to_memory(output_table_name)
        self.mock_make_query_table_management.assert_called_with(input_table, in_memory_table, "", "", fields, "")



