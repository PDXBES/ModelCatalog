from businessclasses.generic_class_factory import GenericClassFactory
from businessclasses.config import Config
from object_data_io import ObjectDataIo
from rrad_mapping_db_data_io import RradMappingDbDataIo
from businessclasses.mapping_area import MappingArea
from businessclasses.mapping_node import MappingNode
from businessclasses.mapping_link import MappingLink

class MappingSnapshotDataIo(ObjectDataIo):

    def __init__(self, config, rrad_mapping_db_data_io):
        self.config = config
        self.rrad_mapping_db_data_io = rrad_mapping_db_data_io

    def copy_mapping_areas_to_memory(self, mapping_snapshot, output_table_name):
        input_table = self.config.area_results_sde_path
        id_field_name = "Simulation_ID"
        id_list = mapping_snapshot.simulation_ids()
        self.rrad_mapping_db_data_io.copy_to_memory_with_id_filter(input_table, output_table_name, id_field_name, id_list)

    def copy_mapping_nodes_to_memory(self, mapping_snapshot, output_table_name):
        input_table = self.config.node_results_sde_path
        id_field_name = "Simulation_ID"
        id_list = mapping_snapshot.simulation_ids()
        self.rrad_mapping_db_data_io.copy_to_memory_with_id_filter(input_table, output_table_name, id_field_name, id_list)

    def copy_mapping_links_for_capacity_to_memory(self, mapping_snapshot, output_table_name):
        input_table = self.config.link_results_sde_path
        id_field_name = "Simulation_ID"
        id_list = mapping_snapshot.simulation_ids()
        self.rrad_mapping_db_data_io.copy_to_memory_with_id_filter(input_table, output_table_name, id_field_name, id_list)

    def copy_mapping_links_for_rehab_to_memory(self, mapping_snapshot, output_table_name):
        input_table = self.config.rehab_results_sde_path
        id_field_name = "Simulation_ID"
        id_list = mapping_snapshot.simulation_ids()
        self.rrad_mapping_db_data_io.copy_to_memory_with_id_filter(input_table, output_table_name, id_field_name,
                                                                   id_list)

    def append_mapping_links(self, mapping_snapshot):
        field_attribute_lookup = MappingLink.input_field_attribute_lookup()
        template_table_path = self.config.mapping_links_sde_path
        target_path = self.config.mapping_links_sde_path
        object_list = mapping_snapshot.mapping_links
        self.rrad_mapping_db_data_io.append_objects_to_db(object_list,
                                                          field_attribute_lookup,
                                                          template_table_path,
                                                          target_path)

    def append_mapping_nodes(self, mapping_snapshot):
        field_attribute_lookup = MappingNode.input_field_attribute_lookup()
        template_table_path = self.config.mapping_nodes_sde_path
        target_path = self.config.mapping_nodes_sde_path
        object_list = mapping_snapshot.mapping_nodes
        self.rrad_mapping_db_data_io.append_objects_to_db(object_list,
                                                          field_attribute_lookup,
                                                          template_table_path,
                                                          target_path)

    def append_mapping_areas(self, mapping_snapshot):
        field_attribute_lookup = MappingArea.input_field_attribute_lookup()
        template_table_path = self.config.mapping_areas_sde_path
        target_path = self.config.mapping_areas_sde_path
        object_list = mapping_snapshot.mapping_areas
        self.rrad_mapping_db_data_io.append_objects_to_db(object_list,
                                                          field_attribute_lookup,
                                                          template_table_path,
                                                          target_path)
