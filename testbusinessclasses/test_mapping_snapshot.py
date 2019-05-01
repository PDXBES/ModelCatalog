from unittest import TestCase
import mock
from testbusinessclasses.mock_config import MockConfig
from businessclasses.mapping_snapshot import MappingSnapshot
from businessclasses.simulation import Simulation
from businessclasses.mapping_snapshot_exception import NoSimulationsInMappingSnapshotException
from dataio.rrad_mapping_db_data_io import RradMappingDbDataIo

class TestMappingSnapshot(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.mock_simulation1 = mock.MagicMock(Simulation)
        self.mock_simulation1.id = 1
        self.mock_simulation2 = mock.MagicMock(Simulation)
        self.mock_simulation2.id = 2
        self.mock_simulation_list = [self.mock_simulation1, self.mock_simulation2]

        self.mapping_snapshot = MappingSnapshot(self.config)
        self.mapping_snapshot.simulations = self.mock_simulation_list

        self.mock_rrad_mapping_db_data_io = mock.MagicMock(RradMappingDbDataIo)

        self.patch_copy_mapping_areas_to_memory = mock.patch("dataio.mapping_snapshot_data_io.MappingSnapshotDataIo.copy_mapping_areas_to_memory")
        self.mock_copy_mapping_areas_to_memory = self.patch_copy_mapping_areas_to_memory.start()

    def tearDown(self):
        self.mock_copy_mapping_areas_to_memory = self.patch_copy_mapping_areas_to_memory.stop()

    def test_simulation_ids_returns_list_of_correct_simulations(self):
        simulation_ids = self.mapping_snapshot.simulation_ids()
        self.assertEqual([1, 2], simulation_ids)

    def test_simulation_ids_no_simulations_in_snapshot_throws_exception(self):
        self.mapping_snapshot.simulations = []
        with self.assertRaises(NoSimulationsInMappingSnapshotException):
            self.mapping_snapshot.simulation_ids()

    def test_create_mapping_areas_calls_copy_mapping_areas_to_memory_with_correct_arguments(self):
        self.mapping_snapshot.create_mapping_areas(self.mock_rrad_mapping_db_data_io, self.mapping_snapshot.simulations)
        self.mock_copy_mapping_areas_to_memory.assert_called_with("mapping_snapshot", "output_table_name")

