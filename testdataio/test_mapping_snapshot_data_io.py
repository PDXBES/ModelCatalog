import mock
from unittest import TestCase
from testbusinessclasses.mock_config import MockConfig
from dataio.rrad_mapping_db_data_io import RradMappingDbDataIo
from dataio.mapping_snapshot_data_io import MappingSnapshotDataIo
from businessclasses.mapping_snapshot import MappingSnapshot

class TestMappingSnapshotDataIo(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.rrad_mapping_data_io = RradMappingDbDataIo(self.config)
        self.mapping_snapshot_data_io = MappingSnapshotDataIo(self.config, self.rrad_mapping_data_io)
        self.mock_mapping_snapshot = mock.MagicMock(MappingSnapshot)

        self.patch_id_list = mock.patch.object(self.mock_mapping_snapshot, "id_list")
        self.mock_id_list = self.patch_id_list.start()

        self.mock_id_list.return_value = "id_list"


        self.patch_copy_to_memory_with_id_filter = mock.patch("dataio.rrad_mapping_db_data_io.RradMappingDbDataIo.copy_to_memory_with_id_filter")
        self.mock_copy_to_memory_with_id_filter = self.patch_copy_to_memory_with_id_filter.start()

    def tearDown(self):
        self.mock_copy_to_memory_with_id_filter = self.patch_copy_to_memory_with_id_filter.stop()
        self.mock_id_list = self.patch_id_list.stop()


    def test_copy_mapping_areas_to_memory_calls_copy_to_memory_with_id_filter_with_correct_arguments(self):
        input_table = "mapping_areas_sde_path"
        in_memory_output_table_name = "in_memory_table"
        id_field_name = "Simulation_ID" \
                        ""
        id_list = "id_list"
        self.mapping_snapshot_data_io.copy_mapping_areas_to_memory(self.mock_mapping_snapshot, in_memory_output_table_name)
        self.mock_copy_to_memory_with_id_filter.assert_called_with(input_table, in_memory_output_table_name, id_field_name, id_list)