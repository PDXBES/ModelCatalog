from unittest import TestCase
from rehab_data_io import RehabDataIO
import mock
from mock_config import MockConfig

class TestRehabDataIO(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.rehab_data_io = RehabDataIO(self.config )
        self.patch_make_feature_layer = mock.patch("arcpy.MakeFeatureLayer_management")
        self.patch_select_by_attribute = mock.patch("arcpy.SelectLayerByAttribute_management")
        self.mock_make_feature_layer = self.patch_make_feature_layer.start()
        self.mock_select_by_attribute = self.patch_select_by_attribute.start()

        self.patch_delete_field = mock.patch("arcpy.DeleteField_management")
        self.mock_delete_field = self.patch_delete_field.start()

        self.patch_join_field = mock.patch("arcpy.JoinField_management")
        self.mock_join_field = self.patch_join_field.start()

        self.patch_append = mock.patch("arcpy.Append_management")
        self.mock_append = self.patch_append.start()

        self.patch_copy_features = mock.patch("arcpy.CopyFeatures_management")
        self.mock_copy_features = self.patch_copy_features.start()

        self.patch_copy_rows = mock.patch("arcpy.CopyRows_management")
        self.mock_copy_rows = self.patch_copy_rows.start()

        self.patch_table_to_table = mock.patch("arcpy.TableToTable_conversion")
        self.mock_table_to_table = self.patch_table_to_table.start()

        self.patch_select_nbcr_data_pipes = mock.patch("select_nbcr_data_pipes")
        self.mock_select_nbcr_data_pipes = self.patch_select_nbcr_data_pipes.start()

    def tearDown(self):
        self.mock_make_feature_layer = self.patch_make_feature_layer.stop()
        self.mock_select_by_attribute = self.patch_select_by_attribute.stop()
        self.mock_delete_field = self.patch_delete_field.stop()
        self.mock_join_field = self.patch_join_field.stop()
        self.mock_append = self.patch_append.stop()
        self.mock_copy_features = self.patch_copy_features.stop()
        self.mock_copy_rows = self.patch_copy_rows.stop()
        self.mock_table_to_table = self.patch_table_to_table.stop()
        self.mock_select_nbcr_data_pipes = self.patch_select_nbcr_data_pipes.stop()

    def test_select_nbcr_data_pipes_calls_make_feature_layer(self):
        self.rehab_data_io._select_nbcr_data_pipes()
        self.assertTrue(self.mock_make_feature_layer.called)


    def test_select_nbcr_data_pipes_called_with_correct_arguments(self):
        self.rehab_data_io._select_nbcr_data_pipes()
        self.mock_make_feature_layer.assert_called_with("rehab_nbcr_data_sde_path",
                                                         "nbcr_data_whole_pipes_layer",
                                                         "hservstat not in ( 'ABAN' , 'TBAB' , 'DNE' ) and cutno = 0 and compkey is not Null",
                                                         "in_memory")

    def test_create_pipe_feature_class_calls_copy_feature(self):
        self.rehab_data_io._create_pipe_feature_class()
        self.assertTrue(self.mock_copy_features.called)

    def test_create_pipe_feature_class_called_with_correct_arguments(self):
        self.rehab_data_io._create_pipe_feature_class()
        self.mock_copy_features.assert_called_with("nbcr_data_whole_pipes_layer",
                                                   "in_memory/nbcr_data_whole_pipes")

    def test_create_branches_feature_class_calls_copy_rows(self):
        self.rehab_data_io.create_branches_feature_class()
        self.assertTrue(self.mock_copy_rows.called)


    def test_create_branches_feature_class_called_with_correct_arguments(self):
        self.rehab_data_io.create_branches_feature_class()
        self.mock_copy_rows.assert_called_with("rehab_branches_sde_path",
                                                   "in_memory/rehab_branches")

    def test_delete_nbcr_data_bpw_field_calls_delete_field_management(self):
        self.rehab_data_io.delete_nbcr_data_bpw_field()
        self.assertTrue(self.mock_delete_field.called)

    def test_delete_nbcr_data_bpw_field_called_with_correct_arguments(self):
        self.rehab_data_io.delete_nbcr_data_bpw_field()
        self.mock_delete_field.assert_called_with("in_memory/nbcr_data_whole_pipes",
                                                  "BPW")

    def test_add_bpw_from_branches_calls_join_field_management(self):
        self.rehab_data_io.add_bpw_from_branches()
        self.assertTrue(self.mock_join_field.called)

    def test_add_bpw_from_branches_called_with_correct_arguments(self):
        self.rehab_data_io.add_bpw_from_branches()
        self.mock_join_field.assert_called_with("in_memory/nbcr_data_whole_pipes",
                                                "compkey",
                                                "in_memory/rehab_branches",
                                                "compkey",
                                                "BPW")

    def test_append_whole_pipes_to_rehab_results_calls_append_management(self):
        self.rehab_data_io.append_whole_pipes_to_rehab_results()
        self.assertTrue(self.mock_append.called)

    def test_append_whole_pipes_to_rehab_results_called_with_correct_arguments(self):
        self.rehab_data_io.append_whole_pipes_to_rehab_results()
        self.mock_append.assert_called_with("in_memory/nbcr_data_whole_pipes",
                                            "rehab_results_sde_path",
                                            "NO_TEST")

    def test_convert_nbcr_data_to_table_calls_table_to_table(self):
        self.rehab_data_io.convert_nbcr_data_to_table()
        self.assertTrue(self.mock_table_to_table.called)

    def test_convert_nbcr_data_to_table_called_with_correct_arguments(self):
        self.rehab_data_io.convert_nbcr_data_to_table()
        self.mock_table_to_table.assert_called_with("rehab_nbcr_data_sde_path",
                                             "in_memory",
                                             "nbcr_data_whole_pipe_table",
                                             "hservstat not in ( 'ABAN' , 'TBAB' , 'DNE' ) and cutno = 0 and compkey is not Null")

    def test_convert_nbcr_data_to_table_calls_select_nbcr_data_pipes(self):
        self.rehab_data_io.convert_nbcr_data_to_table()
        self.assertTrue(self.mock_select_nbcr_data_pipes.called)

#TODO: test for functions in convert_nbcr_data_to_table