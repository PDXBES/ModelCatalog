from unittest import TestCase
from dataio.rehab_data_io_new import RehabDataIo

import mock
from testbusinessclasses.mock_config import MockConfig
from businessclasses.rehab import Rehab
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

        self.patch_join_field_management = mock.patch("arcpy.JoinField_management")
        self.mock_join_field_management = self.patch_join_field_management.start()

        self.patch_add_parent_id = mock.patch("dataio.rrad_db_data_io.RradDbDataIo.add_parent_id")
        self.mock_add_parent_id = self.patch_add_parent_id.start()

        self.mock_rehab = mock.MagicMock(Rehab)
        self.mock_rehab.id = 1

    def tearDown(self):
        self.mock_make_query_table_management = self.patch_make_query_table.stop()
        self.mock_join_field_management = self.patch_join_field_management.stop()
        self.mock_add_parent_id = self.patch_add_parent_id.stop()

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

    def test_copy_rehab_results_to_memory_calls_copy_rehab_results_from_nbcr_data_to_memory_with_correct_arguments(self):
        output_table_name = "output_table_name"
        with mock.patch.object(self.rehab_data_io, "copy_rehab_results_from_nbcr_data_to_memory") as mock_copy_rehab_results_from_nbcr_data_to_memory:
            with mock.patch.object(self.rehab_data_io,
                                   "copy_rehab_results_from_rehab_branches_to_memory"):
                with mock.patch.object(self.rehab_data_io,
                                       "copy_rehab_results_from_tv_ratings_to_memory"):
                    self.rehab_data_io.copy_rehab_results_to_memory(output_table_name, self.mock_rehab)
                    mock_copy_rehab_results_from_nbcr_data_to_memory.assert_called_with(output_table_name)

    def test_copy_rehab_results_to_memory_calls_copy_rehab_results_from_rehab_branches_to_memory_with_correct_arguments(self):
        output_table_name = "output_table_name"
        with mock.patch.object(self.rehab_data_io,
                               "copy_rehab_results_from_nbcr_data_to_memory"):
            with mock.patch.object(self.rehab_data_io,
                                   "copy_rehab_results_from_rehab_branches_to_memory") as mock_copy_rehab_results_from_rehab_branches_to_memory:
                with mock.patch.object(self.rehab_data_io,
                                       "copy_rehab_results_from_tv_ratings_to_memory"):
                    self.rehab_data_io.copy_rehab_results_to_memory(output_table_name, self.mock_rehab)
                    mock_copy_rehab_results_from_rehab_branches_to_memory.assert_called_with("rehab_results_from_rehab_branches")

    def test_copy_rehab_results_to_memory_calls_copy_rehab_results_from_tv_ratings_to_memory_with_correct_arguments(self):
        output_table_name = "output_table_name"
        with mock.patch.object(self.rehab_data_io,
                               "copy_rehab_results_from_nbcr_data_to_memory"):
            with mock.patch.object(self.rehab_data_io,
                                   "copy_rehab_results_from_rehab_branches_to_memory"):
                with mock.patch.object(self.rehab_data_io,
                                       "copy_rehab_results_from_tv_ratings_to_memory") as mock_copy_rehab_results_from_tv_ratings_to_memory:
                    self.rehab_data_io.copy_rehab_results_to_memory(output_table_name, self.mock_rehab)
                    mock_copy_rehab_results_from_tv_ratings_to_memory.assert_called_with("rehab_results_from_tv_ratings")

    def test_copy_rehab_results_to_memory_calls_join_field_management_with_correct_arguments(self):
        output_table_name = "output_table_name"
        fields_rehab_branches = ["BPW"]
        fields_tv_ratings = ["ROOT_RATING"]
        with mock.patch.object(self.rehab_data_io,
                               "copy_rehab_results_from_nbcr_data_to_memory"):
            with mock.patch.object(self.rehab_data_io,
                                   "copy_rehab_results_from_rehab_branches_to_memory"):
                with mock.patch.object(self.rehab_data_io,
                                       "copy_rehab_results_from_tv_ratings_to_memory"):
                    self.rehab_data_io.copy_rehab_results_to_memory(output_table_name, self.mock_rehab)
                    self.mock_join_field_management.assert_has_calls([mock.call("in_memory\\output_table_name", "compkey",
                                                                         "in_memory\\rehab_results_from_rehab_branches", "compkey", fields_rehab_branches),
                                                                      mock.call("in_memory\\output_table_name", "GLOBALID",
                                                                              "in_memory\\rehab_results_from_tv_ratings",
                                                                              "GLOBALID", fields_tv_ratings)
                                                                      ])

    def test_copy_rehab_results_to_memory_calls_add_parent_id_with_correct_arguments(self):
        output_table_name = "output_table_name"
        with mock.patch.object(self.rehab_data_io,
                               "copy_rehab_results_from_nbcr_data_to_memory"):
            with mock.patch.object(self.rehab_data_io,
                                   "copy_rehab_results_from_rehab_branches_to_memory"):
                with mock.patch.object(self.rehab_data_io,
                                       "copy_rehab_results_from_tv_ratings_to_memory"):
                    self.rehab_data_io.copy_rehab_results_to_memory(output_table_name, self.mock_rehab)
                    self.mock_add_parent_id.assert_called_with(output_table_name, "rehab_id", 1)

