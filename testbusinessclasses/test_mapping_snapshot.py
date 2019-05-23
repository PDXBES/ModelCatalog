from unittest import TestCase
import mock
from testbusinessclasses.mock_config import MockConfig
from businessclasses.mapping_snapshot import MappingSnapshot
from businessclasses.simulation import Simulation
from businessclasses.mapping_snapshot_exception import NoSimulationsInMappingSnapshotException
from dataio.mapping_snapshot_data_io import MappingSnapshotDataIo
from dataio.rrad_mapping_db_data_io import RradMappingDbDataIo
from businessclasses.mapping_area import MappingArea
from businessclasses.mapping_node import MappingNode
from businessclasses.mapping_link import MappingLink

class TestMappingSnapshot(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.mock_simulation1 = mock.MagicMock(Simulation)
        self.mock_simulation1.id = 1
        self.mock_simulation1.sim_desc = "sim_desc_1"
        self.mock_simulation2 = mock.MagicMock(Simulation)
        self.mock_simulation2.id = 2
        self.mock_simulation2.sim_desc = "sim_desc_2"

        self.mock_simulation_list = [self.mock_simulation1, self.mock_simulation2]

        self.mapping_snapshot = MappingSnapshot(self.config)
        self.mapping_snapshot.simulations = self.mock_simulation_list
        self.mapping_snapshot.id = 666

        self.mapping_node_1 = mock.MagicMock(MappingNode)
        self.mapping_node_1.simulation_id = 1
        self.mapping_node_1.sim_desc = None
        self.mapping_node_1.snapshot_id = None

        self.mapping_node_2 = mock.MagicMock(MappingNode)
        self.mapping_node_2.simulation_id = 2
        self.mapping_node_2.sim_desc = None
        self.mapping_node_2.snapshot_id = None


        self.mapping_area_1 = mock.MagicMock(MappingArea)
        self.mapping_area_1.sim_desc = None
        self.mapping_area_1.snapshot_id = None
        self.mapping_area_1.simulation_id = 1
        self.mapping_area_2 = mock.MagicMock(MappingArea)
        self.mapping_area_2.sim_desc = None
        self.mapping_area_2.snapshot_id = None
        self.mapping_area_2.simulation_id = 2

        self.mapping_link_1 = mock.MagicMock(MappingLink)
        self.mapping_link_1.sim_desc = None
        self.mapping_link_1.snapshot_id = None
        self.mapping_link_1.simulation_id = 1
        self.mapping_link_2 = mock.MagicMock(MappingLink)
        self.mapping_link_2.sim_desc = None
        self.mapping_link_2.snapshot_id = None
        self.mapping_link_2.simulation_id = 2

        self.mock_rrad_mapping_db_data_io = mock.MagicMock(RradMappingDbDataIo)
        self.mock_rrad_mapping_db_data_io.workspace = "in_memory"

        self.mock_mapping_snapshot_data_io = mock.MagicMock(MappingSnapshotDataIo)
        self.mock_mapping_snapshot_data_io.rrad_mapping_db_data_io = self.mock_rrad_mapping_db_data_io

        self.patch_copy_mapping_areas_to_memory = mock.patch.object(self.mock_mapping_snapshot_data_io, "copy_mapping_areas_to_memory")
        self.mock_copy_mapping_areas_to_memory = self.patch_copy_mapping_areas_to_memory.start()

        self.patch_copy_mapping_nodes_to_memory = mock.patch.object(self.mock_mapping_snapshot_data_io, "copy_mapping_nodes_to_memory")
        self.mock_copy_mapping_nodes_to_memory = self.patch_copy_mapping_nodes_to_memory.start()

        self.patch_create_objects_from_table_with_current_id = mock.patch.object(self.mock_rrad_mapping_db_data_io, "create_objects_from_table_with_current_id")
        self.mock_create_objects_from_table_with_current_id = self.patch_create_objects_from_table_with_current_id.start()

        self.patch_arcpy_delete_management = mock.patch("arcpy.Delete_management")
        self.mock_arcpy_delete_management = self.patch_arcpy_delete_management.start()

        self.patch_copy_mapping_links_for_capacity_to_memory = mock.patch.object(self.mock_mapping_snapshot_data_io, "copy_mapping_links_for_capacity_to_memory")
        self.mock_copy_mapping_links_for_capacity_to_memory = self.patch_copy_mapping_links_for_capacity_to_memory.start()

        self.patch_copy_mapping_links_for_rehab_to_memory = mock.patch.object(self.mock_mapping_snapshot_data_io,
                                                                                 "copy_mapping_links_for_rehab_to_memory")
        self.mock_copy_mapping_links_for_rehab_to_memory = self.patch_copy_mapping_links_for_rehab_to_memory.start()

        self.patch_arcpy_add_join_management = mock.patch("arcpy.AddJoin_management")
        self.mock_arcpy_add_join_management = self.patch_arcpy_add_join_management.start()

    def tearDown(self):
        self.mock_copy_mapping_areas_to_memory = self.patch_copy_mapping_areas_to_memory.stop()
        self.mock_create_objects_from_table_with_current_id = self.patch_create_objects_from_table_with_current_id.stop()
        self.mock_arcpy_delete_management = self.patch_arcpy_delete_management.stop()
        self.mock_copy_mapping_nodes_to_memory = self.patch_copy_mapping_nodes_to_memory.stop()
        self.mock_copy_mapping_links_for_capacity_to_memory = self.patch_copy_mapping_links_for_capacity_to_memory.stop()
        self.mock_copy_mapping_links_for_rehab_to_memory = self.patch_copy_mapping_links_for_rehab_to_memory.stop()
        self.mock_arcpy_add_join_management = self.patch_arcpy_add_join_management.stop()



    def test_simulation_ids_returns_list_of_correct_simulations(self):
        simulation_ids = self.mapping_snapshot.simulation_ids()
        self.assertEqual([1, 2], simulation_ids)

    def test_simulation_ids_no_simulations_in_snapshot_throws_exception(self):
        self.mapping_snapshot.simulations = []
        with self.assertRaises(NoSimulationsInMappingSnapshotException):
            self.mapping_snapshot.simulation_ids()

    def test_create_mapping_areas_calls_copy_mapping_areas_to_memory_with_correct_arguments(self):
        self.mapping_snapshot.create_mapping_areas(self.mock_mapping_snapshot_data_io)
        self.mock_copy_mapping_areas_to_memory.assert_called_with(self.mapping_snapshot, "mapping_area_in_memory_table")

    def test_create_mapping_areas_calls_create_objects_from_table_with_current_id_with_correct_arguments(self):
        self.mapping_snapshot.create_mapping_areas(self.mock_mapping_snapshot_data_io)
        self.mock_create_objects_from_table_with_current_id.assert_called_with("mapping_area", "in_memory\\mapping_area_in_memory_table",
                                                                               MappingArea.rrad_input_field_attribute_lookup())

    def test_create_mapping_areas_calls_arcpy_delete_management_with_correct_arguments(self):
        self.mapping_snapshot.create_mapping_areas(self.mock_mapping_snapshot_data_io)
        self.mock_arcpy_delete_management.assert_called_with("in_memory\\mapping_area_in_memory_table")

    def test_create_mapping_nodes_calls_copy_mapping_areas_to_memory_with_correct_arguments(self):
        self.mapping_snapshot.create_mapping_nodes(self.mock_mapping_snapshot_data_io)
        self.mock_copy_mapping_nodes_to_memory.assert_called_with(self.mapping_snapshot, "mapping_node_in_memory_table")

    def test_create_mapping_nodes_calls_create_objects_from_table_with_current_id_with_correct_arguments(self):
        self.mapping_snapshot.create_mapping_nodes(self.mock_mapping_snapshot_data_io)
        self.mock_create_objects_from_table_with_current_id.assert_called_with("mapping_node", "in_memory\\mapping_node_in_memory_table",
                                                                               MappingNode.rrad_input_field_attribute_lookup())

    def test_create_mapping_nodes_calls_arcpy_delete_management_with_correct_arguments(self):
        self.mapping_snapshot.create_mapping_nodes(self.mock_mapping_snapshot_data_io)
        self.mock_arcpy_delete_management.assert_called_with("in_memory\\mapping_node_in_memory_table")

    def test_join_rehab_and_capacity_in_memory_tables_calls_mapping_links_for_capacity_to_memory_with_correct_arguments(self):
        capacity_rehab_in_memory_table_name = "capacity_rehab_in_memory_table"
        self.mapping_snapshot.join_rehab_and_capacity_in_memory_tables(self.mock_mapping_snapshot_data_io, capacity_rehab_in_memory_table_name)
        self.mock_copy_mapping_links_for_capacity_to_memory.assert_called_with(self.mapping_snapshot,"capacity_rehab_in_memory_table")

    def test_join_rehab_and_capacity_in_memory_tables_calls_mapping_links_for_rehab_to_memory_with_correct_arguments(self):
        capacity_rehab_in_memory_table_name = "capacity_rehab_in_memory_table"
        self.mapping_snapshot.join_rehab_and_capacity_in_memory_tables(self.mock_mapping_snapshot_data_io, capacity_rehab_in_memory_table_name)
        self.mock_copy_mapping_links_for_rehab_to_memory.assert_called_with(self.mapping_snapshot,"rehab_links_in_memory_table")

    def test_join_rehab_and_capacity_in_memory_tables_calls_arcpy_AddJoin_management_with_correct_arguments(self):
        capacity_rehab_in_memory_table_name = "capacity_rehab_in_memory_table"
        self.mapping_snapshot.join_rehab_and_capacity_in_memory_tables(self.mock_mapping_snapshot_data_io, capacity_rehab_in_memory_table_name)
        self.mock_arcpy_add_join_management.assert_called_with("in_memory\\capacity_rehab_in_memory_table", "dme_global_id", "in_memory\\rehab_links_in_memory_table", "GLOBALID", "KEEP_ALL")

    def test_create_mapping_links_calls_join_rehab_and_capacity_in_memory_tables_with_correct_arguments(self):
        with mock.patch.object(self.mapping_snapshot, "join_rehab_and_capacity_in_memory_tables") as mock_join_rehab_and_capacity_in_memory_tables:
            self.mapping_snapshot.create_mapping_links(self.mock_mapping_snapshot_data_io)
            mock_join_rehab_and_capacity_in_memory_tables.assert_called_with(self.mock_mapping_snapshot_data_io, 'mapping_link_in_memory_table')

    def test_create_mapping_links_calls_create_objects_from_table_with_current_id_with_correct_arguments(self):
        self.mapping_snapshot.create_mapping_links(self.mock_mapping_snapshot_data_io)
        self.mock_create_objects_from_table_with_current_id.assert_called_with("mapping_link", "in_memory\\mapping_link_in_memory_table",
                                                                               MappingLink.rrad_field_attribute_lookup())

    def test_create_mapping_links_calls_arcpy_delete_management_with_correct_arguments(self):
        self.mapping_snapshot.create_mapping_links(self.mock_mapping_snapshot_data_io)
        self.mock_arcpy_delete_management.assert_called_with("in_memory\\mapping_link_in_memory_table")

    def test_create_mapping_nodes_returns_mapping_nodes(self):
        self.mock_create_objects_from_table_with_current_id.return_value = [self.mapping_node_1, self.mapping_node_2]
        self.mapping_snapshot.create_mapping_nodes(self.mock_mapping_snapshot_data_io)
        mapping_nodes = self.mapping_snapshot.mapping_nodes
        self.assertEquals(mapping_nodes, [self.mapping_node_1, self.mapping_node_2])

    def test_create_mapping_areas_returns_mapping_areas(self):
        self.mock_create_objects_from_table_with_current_id.return_value = [self.mapping_area_1, self.mapping_area_2]
        self.mapping_snapshot.create_mapping_areas(self.mock_mapping_snapshot_data_io)
        mapping_areas = self.mapping_snapshot.mapping_areas
        self.assertEquals(mapping_areas, [self.mapping_area_1, self.mapping_area_2])

    def test_create_mapping_links_returns_mapping_links(self):
        self.mock_create_objects_from_table_with_current_id.return_value = [self.mapping_link_1, self.mapping_link_2]
        self.mapping_snapshot.create_mapping_links(self.mock_mapping_snapshot_data_io)
        mapping_links = self.mapping_snapshot.mapping_links
        self.assertEquals(mapping_links, [self.mapping_link_1, self.mapping_link_2])

    def test_add_snapshot_id_and_sim_desc_sets_list_of_mapping_objects_with_sim_desc_and_snapshot_id(self):
        self.mapping_snapshot.mapping_nodes = [self.mapping_node_1, self.mapping_node_2]
        self.mapping_snapshot.add_snapshot_id_and_sim_desc(self.mapping_snapshot.mapping_nodes)
        mapping_nodes = self.mapping_snapshot.mapping_nodes
        self.assertEquals(mapping_nodes[0].sim_desc, "sim_desc_1")
        self.assertEquals(mapping_nodes[0].snapshot_id, 666)
        self.assertEquals(mapping_nodes[1].sim_desc, "sim_desc_2")
        self.assertEquals(mapping_nodes[1].snapshot_id, 666)

    def test_create_mapping_nodes_calls_add_snapshot_and_sim_desc_with_mapping_nodes(self):
        self.mock_create_objects_from_table_with_current_id.return_value = [self.mapping_node_1, self.mapping_node_2]
        with mock.patch.object(self.mapping_snapshot, "add_snapshot_id_and_sim_desc") as mock_add_snapshot_id_and_sim_desc:
            self.mapping_snapshot.create_mapping_nodes(self.mock_mapping_snapshot_data_io)
            mock_add_snapshot_id_and_sim_desc.assert_called_with([self.mapping_node_1, self.mapping_node_2])

    def test_create_mapping_links_calls_add_snapshot_and_sim_desc_with_mapping_links(self):
        self.mock_create_objects_from_table_with_current_id.return_value = [self.mapping_link_1, self.mapping_link_2]
        with mock.patch.object(self.mapping_snapshot, "add_snapshot_id_and_sim_desc") as mock_add_snapshot_id_and_sim_desc:
            self.mapping_snapshot.create_mapping_links(self.mock_mapping_snapshot_data_io)
            mock_add_snapshot_id_and_sim_desc.assert_called_with([self.mapping_link_1, self.mapping_link_2])

    def test_create_mapping_areas_calls_add_snapshot_and_sim_desc_with_mapping_areas(self):
        self.mock_create_objects_from_table_with_current_id.return_value = [self.mapping_area_1, self.mapping_area_2]
        with mock.patch.object(self.mapping_snapshot, "add_snapshot_id_and_sim_desc") as mock_add_snapshot_id_and_sim_desc:
            self.mapping_snapshot.create_mapping_areas(self.mock_mapping_snapshot_data_io)
            mock_add_snapshot_id_and_sim_desc.assert_called_with([self.mapping_area_1, self.mapping_area_2])
