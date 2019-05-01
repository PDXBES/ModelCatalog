from businessclasses.generic_class_factory import GenericClassFactory
from businessclasses.config import Config
from object_data_io import ObjectDataIo
from rrad_mapping_db_data_io import RradMappingDbDataIo

class MappingSnapshotDataIo(ObjectDataIo):

    def __init__(self, config, rrad_mapping_data_io):
        self.config = config
        self.rrad_mapping_data_io = rrad_mapping_data_io

    def copy_mapping_areas_to_memory(self, mapping_snapshot, output_table_name):
        input_table = self.config.mapping_areas_sde_path
        id_field_name = "Simulation_ID"
        id_list = mapping_snapshot.simulation_ids()
        self.rrad_mapping_data_io.copy_to_memory_with_id_filter(input_table, output_table_name, id_field_name, id_list)

    def copy_mapping_nodes_to_memory(self, mapping_snapshot, output_table_name):
        input_table = self.config.mapping_nodes_sde_path
        id_field_name = "Simulation_ID"
        id_list = mapping_snapshot.simulation_ids()
        self.rrad_mapping_data_io.copy_to_memory_with_id_filter(input_table, output_table_name, id_field_name, id_list)

    def append_mapping_links(self):
        pass

    def append_mapping_nodes(self):
        pass

    def append_mapping_areas(self):
        pass