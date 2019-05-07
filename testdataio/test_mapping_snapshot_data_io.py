import mock
from unittest import TestCase
from testbusinessclasses.mock_config import MockConfig
from dataio.rrad_mapping_db_data_io import RradMappingDbDataIo
from dataio.mapping_snapshot_data_io import MappingSnapshotDataIo
from businessclasses.mapping_snapshot import MappingSnapshot
from businessclasses.mapping_area import MappingArea
from businessclasses.mapping_node import MappingNode
from businessclasses.mapping_link import MappingLink

class TestMappingSnapshotDataIo(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.rrad_mapping_db_data_io = RradMappingDbDataIo(self.config)
        self.mapping_snapshot_data_io = MappingSnapshotDataIo(self.config, self.rrad_mapping_db_data_io)
        self.mock_mapping_snapshot = mock.MagicMock(MappingSnapshot)

        self.simulation_ids = mock.patch.object(self.mock_mapping_snapshot, "simulation_ids")
        self.simulation_ids = self.simulation_ids.start()

        self.simulation_ids.return_value = "id_list"

        self.patch_copy_to_memory_with_id_filter = mock.patch("dataio.rrad_mapping_db_data_io.RradMappingDbDataIo.copy_to_memory_with_id_filter")
        self.mock_copy_to_memory_with_id_filter = self.patch_copy_to_memory_with_id_filter.start()

        self.patch_append_objects_to_db = mock.patch("dataio.rrad_mapping_db_data_io.DbDataIo.append_objects_to_db")
        self.mock_append_objects_to_db = self.patch_append_objects_to_db.start()

    def tearDown(self):
        self.mock_copy_to_memory_with_id_filter = self.patch_copy_to_memory_with_id_filter.stop()
        self.simulation_ids = self.simulation_ids.stop()
        self.mock_append_objects_to_db = self.patch_append_objects_to_db.stop()

    def test_copy_mapping_areas_to_memory_calls_copy_to_memory_with_id_filter_with_correct_arguments(self):
        input_table = "mapping_areas_sde_path"
        in_memory_output_table_name = "in_memory_table"
        id_field_name = "Simulation_ID"
        id_list = "id_list"
        self.mapping_snapshot_data_io.copy_mapping_areas_to_memory(self.mock_mapping_snapshot, in_memory_output_table_name)
        self.mock_copy_to_memory_with_id_filter.assert_called_with(input_table, in_memory_output_table_name, id_field_name, id_list)

    def test_copy_mapping_nodes_to_memory_calls_copy_to_memory_with_id_filter_with_correct_arguments(self):
        input_table = "mapping_nodes_sde_path"
        in_memory_output_table_name = "in_memory_table"
        id_field_name = "Simulation_ID"
        id_list = "id_list"
        self.mapping_snapshot_data_io.copy_mapping_nodes_to_memory(self.mock_mapping_snapshot, in_memory_output_table_name)
        self.mock_copy_to_memory_with_id_filter.assert_called_with(input_table, in_memory_output_table_name, id_field_name, id_list)

    def test_append_mapping_areas_calls_append_objects_to_db_with_correct_arguments(self):
        self.mapping_snapshot_data_io.append_mapping_areas("object_list")
        self.mock_append_objects_to_db.assert_called_with("object_list",
                                                          MappingArea.input_field_attribute_lookup(),
                                                          "mapping_areas_sde_path",
                                                          "mapping_areas_sde_path")

    def test_append_mapping_nodes_calls_append_objects_to_db_with_correct_arguments(self):
        self.mapping_snapshot_data_io.append_mapping_nodes("object_list")
        self.mock_append_objects_to_db.assert_called_with("object_list",
                                                          MappingNode.input_field_attribute_lookup(),
                                                          "mapping_nodes_sde_path",
                                                          "mapping_nodes_sde_path")

    def test_copy_mapping_links_for_capacity_to_memory_calls_copy_to_memory_with_id_filter_with_correct_arguments(self):
        input_table = "link_results_sde_path"
        in_memory_output_table_name = "in_memory_table"
        id_field_name = "Simulation_ID"
        id_list = "id_list"
        self.mapping_snapshot_data_io.copy_mapping_links_for_capacity_to_memory(self.mock_mapping_snapshot,
                                                                   in_memory_output_table_name)
        self.mock_copy_to_memory_with_id_filter.assert_called_with(input_table, in_memory_output_table_name,
                                                                   id_field_name, id_list)

    def test_copy_mapping_links_for_rehab_to_memory_calls_copy_to_memory_with_id_filter_with_correct_arguments(self):
        input_table = "rehab_results_sde_path"
        in_memory_output_table_name = "in_memory_table"
        id_field_name = "Simulation_ID"
        id_list = "id_list"
        self.mapping_snapshot_data_io.copy_mapping_links_for_rehab_to_memory(self.mock_mapping_snapshot,
                                                                   in_memory_output_table_name)
        self.mock_copy_to_memory_with_id_filter.assert_called_with(input_table, in_memory_output_table_name,
                                                                   id_field_name, id_list)

    def test_append_mapping_links_calls_append_objects_to_db_with_correct_arguments(self):
        self.mapping_snapshot_data_io.append_mapping_links("object_list")
        self.mock_append_objects_to_db.assert_called_with("object_list",
                                                          MappingLink.input_field_attribute_lookup(),
                                                          "mapping_links_sde_path",
                                                          "mapping_links_sde_path")