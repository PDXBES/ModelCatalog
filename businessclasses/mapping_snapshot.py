from config import Config
import arcpy
from generic_object import GenericObject
from businessclasses.mapping_node import MappingNode
from businessclasses.mapping_area import MappingArea
from businessclasses.mapping_link import MappingLink
from collections import OrderedDict
from businessclasses.mapping_snapshot_exception import NoSimulationsInMappingSnapshotException

try:
    from typing import List, Any
except:
    pass

class MappingSnapshot(GenericObject):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.id = None
        self.type = None
        self.simulations = []
        self.mapping_links = []
        self.mapping_nodes = []
        self.mapping_areas = []
        self.snapshot_id = None
        self.snapshot_type = None
        self.logic = None
        self.requested_by = None
        self.created_by = None

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Snapshot_ID"] = "snapshot_id"
        field_attribute_lookup["Snapshot_Type"] = "snapshot_type"
        field_attribute_lookup["Logic"] = "logic"
        field_attribute_lookup["Requested_by"] = "requested_by"
        field_attribute_lookup["Created_by"] = "created_by"
        return field_attribute_lookup

    def join_rehab_and_capacity_in_memory_tables(self, mapping_snapshot_data_io):
        capacity_output_table_name = "capacity_links_in_memory_table"
        rehab_output_table_name = "rehab_links_in_memory_table"
        capacity_global_id_field = "dme_global_id"
        rehab_global_id_field = "GLOBALID"
        join_type = "KEEP_ALL"
        mapping_snapshot_data_io.copy_mapping_links_for_capacity_to_memory(self, capacity_output_table_name)
        mapping_snapshot_data_io.copy_mapping_links_for_rehab_to_memory(self, rehab_output_table_name)
        arcpy.AddJoin_management(capacity_output_table_name, capacity_global_id_field, rehab_output_table_name, rehab_global_id_field, join_type)

    def create_mapping_links(self, mapping_snapshot_data_io):
        workspace = mapping_snapshot_data_io.rrad_mapping_db_data_io.workspace
        output_table_name = "mapping_link_in_memory_table"
        in_memory_table = workspace + "\\" + output_table_name
        self.join_rehab_and_capacity_in_memory_tables(mapping_snapshot_data_io)
        self.mapping_links = mapping_snapshot_data_io.rrad_mapping_db_data_io.create_objects_from_table_with_current_id(in_memory_table,
                                                                                                   "mapping_link",
                                                                                                   MappingLink.rrad_field_attribute_lookup())
        arcpy.Delete_management(in_memory_table)

    def create_mapping_nodes(self, mapping_snapshot_data_io):
        workspace = mapping_snapshot_data_io.rrad_mapping_db_data_io.workspace
        output_table_name = "mapping_node_in_memory_table"
        in_memory_table = workspace + "\\" + output_table_name
        mapping_snapshot_data_io.copy_mapping_nodes_to_memory(self, output_table_name)
        self.mapping_nodes = mapping_snapshot_data_io.rrad_mapping_db_data_io.create_objects_from_table_with_current_id(in_memory_table,
                                                                                                    "mapping_node",
                                                                                                    MappingNode.rrad_input_field_attribute_lookup())
        arcpy.Delete_management(in_memory_table)

    def create_mapping_areas(self, mapping_snapshot_data_io):
        workspace = mapping_snapshot_data_io.rrad_mapping_db_data_io.workspace
        output_table_name = "mapping_area_in_memory_table"
        in_memory_table = workspace + "\\" + output_table_name
        mapping_snapshot_data_io.copy_mapping_areas_to_memory(self, output_table_name)
        self.mapping_areas = mapping_snapshot_data_io.rrad_mapping_db_data_io.create_objects_from_table_with_current_id(in_memory_table,
                                                                                                   "mapping_area",
                                                                                                   MappingArea.rrad_input_field_attribute_lookup())
        arcpy.Delete_management(in_memory_table)


    def simulation_ids(self):
        simulation_ids = []
        if len(self.simulations) == 0 or self.simulations is None:
            raise NoSimulationsInMappingSnapshotException
        else:
            for simulation in self.simulations:
                simulation_ids.append(simulation.id)
            return simulation_ids

