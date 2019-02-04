from unittest import TestCase
from dataio.rehab_data_io import RehabDataIO
import mock
from testbusinessclasses.mock_config import MockConfig
from businessclasses.rehab import Rehab
import arcpy
from businessclasses.pipe import Pipe

class TestRehabDataIO(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.mock_rehab = mock.MagicMock(Rehab)

        self.rehab_data_io = RehabDataIO(self.config)
        self.patch_make_feature_layer = mock.patch("arcpy.MakeFeatureLayer_management")
        self.patch_select_by_attribute = mock.patch("arcpy.SelectLayerByAttribute_management")
        self.mock_make_feature_layer = self.patch_make_feature_layer.start()
        self.mock_select_by_attribute = self.patch_select_by_attribute.start()

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

        self.patch_da_editor = mock.patch("arcpy.da.Editor")
        self.mock_da_editor = self.patch_da_editor.start()

        self.patch_da_search_cursor = mock.patch("arcpy.da.SearchCursor")
        self.mock_da_search_cursor = self.patch_da_search_cursor.start()

        self.mock_cursor = mock.MagicMock(arcpy.da.InsertCursor) #Must be created before patching arcpy.da.InsertCursor

        self.patch_da_insert_cursor = mock.patch("arcpy.da.InsertCursor")
        self.mock_da_insert_cursor = self.patch_da_insert_cursor.start()

        self.patch_da_delete_field_management = mock.patch("arcpy.DeleteField_management")
        self.mock_da_delete_field_management = self.patch_da_delete_field_management.start()

        self.patch_CreateTable_management = mock.patch("arcpy.CreateTable_management")
        self.mock_CreateTable_management = self.patch_CreateTable_management.start()

        self.patch_list_fields = mock.patch("arcpy.ListFields")
        self.mock_list_fields = self.patch_list_fields.start()

        self.whole_pipe_fields = ["compkey", "bpw", "usnode",
                                  "dsnode", "diamwidth", "length",
                                  "material", "lateralcost", "manholecost",
                                  "asmrecommendednbcr", "asmrecommendedaction",
                                  "apwspot","apwliner", "apwwhole", "lateralcount", "globalid"]

        self.output_pipe_table_fields = ["compkey", "bpw", "usnode",
                                  "dsnode", "diamwidth", "length",
                                  "material", "lateralcost", "manholecost",
                                  "asmrecommendednbcr", "asmrecommendedaction",
                                  "apwspot","apwliner", "apwwhole", "lateralcount", "globalid", "apw", "capitalcost", 
                                         "rehab_id"]

        self.dummy_row_1 = [1, 2, "usnode1",
                                   "dsnode1", 3, 4,
                                   "material1", 5, 6,
                                   7, "asmrecommendedaction1",
                                   9, 10, 11, 12, 13]

        self.dummy_row_2 = [12, 22, "usnode2",
                                   "dsnode2", 32, 42,
                                   "material2", 52, 62,
                                   72, "asmrecommendedaction2",
                                   92, 102, 112, 122, 132]

        self.mock_da_search_cursor.return_value = [self.dummy_row_1, self.dummy_row_2]

        self.rehab_id = 99
        
        self.mock_update_cursor = mock.MagicMock(arcpy.da.InsertCursor)

        self.output_pipes_table_row = [12, 22, "usnode2",
                                   "dsnode2", 32, 42,
                                   "material2", 52, 62,
                                   72, "asmrecommendedaction2",
                                   92, 102, 112, 122, 132, 1000, 3000,111]
        self.mock_pipe = mock.MagicMock(Pipe)

        self.mock_pipe.compkey = self.output_pipes_table_row[0]
        self.mock_pipe.bpw = self.output_pipes_table_row[1]
        self.mock_pipe.usnode = self.output_pipes_table_row[2]
        self.mock_pipe.dsnode = self.output_pipes_table_row[3]
        self.mock_pipe.diamwidth = self.output_pipes_table_row[4]
        self.mock_pipe.length = self.output_pipes_table_row[5]
        self.mock_pipe.material = self.output_pipes_table_row[6]
        self.mock_pipe.lateralcost = self.output_pipes_table_row[7]
        self.mock_pipe.manholecost = self.output_pipes_table_row[8]
        self.mock_pipe.asmrecommendednbcr = self.output_pipes_table_row[9]
        self.mock_pipe.asmrecommendedaction = self.output_pipes_table_row[10]
        self.mock_pipe.apwspot = self.output_pipes_table_row[11]
        self.mock_pipe.apwliner = self.output_pipes_table_row[12]
        self.mock_pipe.apwwhole = self.output_pipes_table_row[13]
        self.mock_pipe.lateralcount = self.output_pipes_table_row[14]
        self.mock_pipe.globalid = self.output_pipes_table_row[15]
        self.mock_pipe.apw = self.output_pipes_table_row[16]
        self.mock_pipe.capitalcost = self.output_pipes_table_row[17]
        self.mock_pipe.rehab_id = self.output_pipes_table_row[18]
        self.mock_rehab.pipes = [self.mock_pipe]

    def tearDown(self):
        self.mock_make_feature_layer = self.patch_make_feature_layer.stop()
        self.mock_select_by_attribute = self.patch_select_by_attribute.stop()
        self.mock_join_field = self.patch_join_field.stop()
        self.mock_append = self.patch_append.stop()
        self.mock_copy_features = self.patch_copy_features.stop()
        self.mock_copy_rows = self.patch_copy_rows.stop()
        self.mock_table_to_table = self.patch_table_to_table.stop()
        self.mock_da_editor = self.patch_da_editor.stop()
        self.mock_da_search_cursor = self.patch_da_search_cursor.stop()
        self.mock_da_insert_cursor = self.patch_da_insert_cursor.stop()
        self.mock_CreateTable_management = self.patch_CreateTable_management.stop()
        self.mock_da_delete_field_management = self.patch_da_delete_field_management.stop()
        self.mock_list_fields = self.patch_list_fields.stop()

    def test_select_nbcr_data_pipes_calls_make_feature_layer_with_correct_arguments(self):
        self.rehab_data_io._select_nbcr_data_pipes()
        self.mock_make_feature_layer.assert_called_with("rehab_nbcr_data_sde_path",
                                                         "nbcr_data_whole_pipes_layer",
                                                         "hservstat not in ( 'ABAN' , 'TBAB' , 'DNE' ) and cutno = 0 and compkey is not Null",
                                                         "in_memory")

    def test_create_pipe_feature_class_calls_copy_features_with_correct_arguments(self):
        self.rehab_data_io._create_pipe_feature_class()
        self.mock_copy_features.assert_called_with("nbcr_data_whole_pipes_layer",
                                                   "in_memory/nbcr_data_whole_pipes")

    def test_create_branches_table_calls_copy_rows_with_correct_arguments(self):
        self.rehab_data_io.create_branches_table()
        self.mock_copy_rows.assert_called_with("rehab_branches_sde_path",
                                                   "in_memory/rehab_branches")

    def test_delete_nbcr_data_bpw_field_calls_delete_field_management_with_correct_arguments(self):
        self.rehab_data_io.delete_nbcr_data_bpw_field("in_memory/nbcr_data_whole_pipes")
        self.mock_da_delete_field_management.assert_called_with("in_memory/nbcr_data_whole_pipes",
                                                  "BPW")

    def test_add_bpw_from_branches_calls_join_field_management_with_correct_arguments(self):
        self.rehab_data_io.nbcr_data_whole_pipe_table_path = "in_memory/nbcr_data_whole_pipes_table"
        self.rehab_data_io.add_bpw_from_branches()
        self.mock_join_field.assert_called_with("in_memory/nbcr_data_whole_pipes_table",
                                                "compkey",
                                                "in_memory/rehab_branches",
                                                "compkey",
                                                "BPW")

    def test_convert_nbcr_data_to_table_calls_table_to_table(self):
        self.rehab_data_io.convert_nbcr_data_to_table()
        self.assertTrue(self.mock_table_to_table.called)

    def test_convert_nbcr_data_to_table_calls_select_nbcr_data_pipes(self):
        with mock.patch.object(self.rehab_data_io, "_select_nbcr_data_pipes") as mock_select_nbcr_data_pipes:
            self.rehab_data_io.convert_nbcr_data_to_table()
            self.assertTrue(mock_select_nbcr_data_pipes.called)

    def test_convert_nbcr_data_to_table_calls_create_pipe_feature_class(self):
        with mock.patch.object(self.rehab_data_io, "_create_pipe_feature_class") as mock_create_pipe_feature_class:
            self.rehab_data_io.convert_nbcr_data_to_table()
            self.assertTrue(mock_create_pipe_feature_class.called)

    def test_convert_nbcr_data_to_table_called_with_correct_arguments(self):
        self.rehab_data_io.convert_nbcr_data_to_table()
        self.mock_table_to_table.assert_called_with("rehab_nbcr_data_sde_path",
                                             "in_memory",
                                             "nbcr_data_whole_pipe_table",
                                             "hservstat not in ( 'ABAN' , 'TBAB' , 'DNE' ) and cutno = 0 and compkey is not Null")

    def test_convert_nbcr_data_to_table_calls_delete_nbcr_data_bpw_field_with_correct_arguments(self):
        with mock.patch.object(self.rehab_data_io, "delete_nbcr_data_bpw_field") as mock_delete_nbcr_data_bpw_field:
            self.rehab_data_io.nbcr_data_whole_pipe_table_path = "nbcr_data_whole_pipe_table_path"
            self.rehab_data_io.convert_nbcr_data_to_table()
            mock_delete_nbcr_data_bpw_field.assert_called_with("nbcr_data_whole_pipe_table_path")

    def test_convert_nbcr_data_to_table_calls_create_branches_table(self):
        with mock.patch.object(self.rehab_data_io, "create_branches_table") as mock_create_branches_table:
            self.rehab_data_io.convert_nbcr_data_to_table()
            self.assertTrue(mock_create_branches_table.called)

    def test_convert_nbcr_data_to_table_calls_add_bpw_from_branches(self):
        with mock.patch.object(self.rehab_data_io, "add_bpw_from_branches") as mock_add_bpw_from_branches:
            self.rehab_data_io.convert_nbcr_data_to_table()
            self.assertTrue(mock_add_bpw_from_branches.called)

    def test_create_pipes_calls_search_cursor_with_correct_arguments(self):
        self.rehab_data_io.nbcr_data_whole_pipe_table_path = "nbcr_data_whole_pipe_table_path"
        self.rehab_data_io.create_pipes(self.rehab_id)
        self.mock_da_search_cursor.assert_called_with("nbcr_data_whole_pipe_table_path",
                                                      self.whole_pipe_fields)

    def test_create_pipes_returns_list_of_two_pipes(self):
        return_pipes = self.rehab_data_io.create_pipes(self.rehab_id)
        self.assertTrue(len(return_pipes),2)

    def test_create_pipes_returns_matching_values(self):
        return_pipes = self.rehab_data_io.create_pipes(self.rehab_id)
        pipe1 = return_pipes[0]
        pipe2 = return_pipes[1]

        self.assertTrue(pipe1.rehab_id, self.rehab_id)
        self.assertTrue(pipe1.compkey, self.dummy_row_1[0])
        self.assertTrue(pipe1.bpw, self.dummy_row_1[1])
        self.assertTrue(pipe1.usnode, self.dummy_row_1[2])
        self.assertTrue(pipe1.dsnode, self.dummy_row_1[3])
        self.assertTrue(pipe1.diamwidth, self.dummy_row_1[4])
        self.assertTrue(pipe1.length, self.dummy_row_1[5])
        self.assertTrue(pipe1.material, self.dummy_row_1[6])
        self.assertTrue(pipe1.lateralcost, self.dummy_row_1[7])
        self.assertTrue(pipe1.manholecost, self.dummy_row_1[8])
        self.assertTrue(pipe1.asmrecommendednbcr, self.dummy_row_1[9])
        self.assertTrue(pipe1.asmrecommendedaction, self.dummy_row_1[10])
        self.assertTrue(pipe1.apwspot, self.dummy_row_1[11])
        self.assertTrue(pipe1.apwliner, self.dummy_row_1[12])
        self.assertTrue(pipe1.apwwhole, self.dummy_row_1[13])
        self.assertTrue(pipe1.lateralcount, self.dummy_row_1[14])
        self.assertTrue(pipe1.globalid, self.dummy_row_1[15])

        self.assertTrue(pipe2.rehab_id, self.rehab_id)
        self.assertTrue(pipe2.compkey, self.dummy_row_2[0])
        self.assertTrue(pipe2.bpw, self.dummy_row_2[1])
        self.assertTrue(pipe2.usnode, self.dummy_row_2[2])
        self.assertTrue(pipe2.dsnode, self.dummy_row_2[3])
        self.assertTrue(pipe2.diamwidth, self.dummy_row_2[4])
        self.assertTrue(pipe2.length, self.dummy_row_2[5])
        self.assertTrue(pipe2.material, self.dummy_row_2[6])
        self.assertTrue(pipe2.lateralcost, self.dummy_row_2[7])
        self.assertTrue(pipe2.manholecost, self.dummy_row_2[8])
        self.assertTrue(pipe2.asmrecommendednbcr, self.dummy_row_2[9])
        self.assertTrue(pipe2.asmrecommendedaction, self.dummy_row_2[10])
        self.assertTrue(pipe2.apwspot, self.dummy_row_2[11])
        self.assertTrue(pipe2.apwliner, self.dummy_row_2[12])
        self.assertTrue(pipe2.apwwhole, self.dummy_row_2[13])
        self.assertTrue(pipe2.lateralcount, self.dummy_row_2[14])
        self.assertTrue(pipe2.globalid, self.dummy_row_2[15])

    def test_write_pipes_to_table_calls_create_table_management_with_correct_arguments(self):
        self.rehab_data_io.write_pipes_to_table(self.mock_rehab)
        self.mock_CreateTable_management.assert_called_with("in_memory", "output_pipes_table","rehab_results_sde_path")

    def test_write_pipes_to_table_calls_insert_cursor_with_correct_arguments(self):
        self.rehab_data_io.write_pipes_to_table(self.mock_rehab)
        self.mock_da_insert_cursor.assert_called_with("in_memory/output_pipes_table", self.output_pipe_table_fields)

    def test_write_pipes_to_table_calls_insert_row_with_correct_arguments(self):
        self.mock_da_insert_cursor.return_value = self.mock_cursor
        self.rehab_data_io.write_pipes_to_table(self.mock_rehab)
        self.mock_cursor.insertRow.assert_called_with(self.output_pipes_table_row)

    def test_delete_fields_calls_list_fields_with_correct_arguments(self):
        feature_class = "feature_class"
        fields_to_keep = ["compkey"]
        self.rehab_data_io.delete_fields(feature_class, fields_to_keep)
        self.mock_list_fields.assert_called_with("feature_class")

    def test_delete_fields_calls_delete_field_management_if_field_not_in_keep_fields(self):
        feature_class = "feature_class"
        fields_to_keep = ["compkey"]
        mock_field_1 = mock.MagicMock(arcpy.Field)
        mock_field_2 = mock.MagicMock(arcpy.Field)
        mock_field_3 = mock.MagicMock(arcpy.Field)
        mock_field_1.name = "apw"
        mock_field_1.type = "not geometry"
        mock_field_2.name = "@Shape"
        mock_field_2.type = "Geometry"
        mock_field_3.name = "compkey"
        mock_field_3.type = "not Geometry"
        self.mock_list_fields.return_value = [mock_field_1, mock_field_2, mock_field_3]
        self.rehab_data_io.delete_fields(feature_class, fields_to_keep)
        self.assertTrue(self.mock_da_delete_field_management.called)

    def test_delete_fields_calls_delete_field_management_if_field_not_in_geometry(self):
        feature_class = "feature_class"
        fields_to_keep = ["compkey"]
        mock_field_2 = mock.MagicMock(arcpy.Field)
        mock_field_2.name = "@Shape"
        mock_field_2.type = "Geometry"
        self.mock_list_fields.return_value = [mock_field_2]
        self.rehab_data_io.delete_fields(feature_class, fields_to_keep)
        self.assertFalse(self.mock_da_delete_field_management.called)

    def test_delete_fields_calls_delete_field_management_if_field_not_in_oid(self):
        feature_class = "feature_class"
        fields_to_keep = ["compkey"]
        mock_field_2 = mock.MagicMock(arcpy.Field)
        mock_field_2.name = "ID"
        mock_field_2.type = "OID"
        self.mock_list_fields.return_value = [mock_field_2]
        self.rehab_data_io.delete_fields(feature_class, fields_to_keep)
        self.assertFalse(self.mock_da_delete_field_management.called)

    def test_delete_specified_fields_calls_list_fields_with_correct_arguments(self):
        feature_class = "feature_class"
        fields_to_delete = ["@shape"]
        self.rehab_data_io.delete_fields(feature_class, fields_to_delete)
        self.mock_list_fields.assert_called_with("feature_class")

    def test_delete_specified_fields_calls_delete_field_management(self):
        feature_class = "feature_class"
        fields_to_delete = ["@shape"]
        mock_field_1 = mock.MagicMock(arcpy.Field)
        mock_field_1.name = "@shape"
        mock_field_1.type = "@geometry"
        self.mock_list_fields.return_value = [mock_field_1]
        self.rehab_data_io.delete_specified_fields(feature_class, fields_to_delete )

    def test_join_output_pipe_table_and_geometry_calls_join_field_with_correct_arguments(self):
        self.active_whole_pipe_feature_class_path = "in_memory/nbcr_data_whole_pipes"
        self.output_pipes_table_path = "in_memory/output_pipes_table"
        self.rehab_data_io.join_output_pipe_table_and_geometry()
        self.mock_join_field.assert_called_with("in_memory/nbcr_data_whole_pipes",
                                                "compkey",
                                                "in_memory/output_pipes_table",
                                                "compkey")

    def test_append_whole_pipes_to_rehab_results_called_with_correct_arguments(self):
        self.rehab_data_io.append_whole_pipes_to_rehab_results()
        self.mock_append.assert_called_with("in_memory/nbcr_data_whole_pipes",
                                            "rehab_results_sde_path",
                                            "NO_TEST")