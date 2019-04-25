from businessclasses.generic_class_factory import GenericClassFactory
from businessclasses.config import Config
from businessclasses.mapping_snapshot import MappingSnapshot
from businessclasses.mapping_node import MappingNode
from businessclasses.mapping_link import MappingLink
from businessclasses.mapping_area import MappingArea

from db_data_io import DbDataIo
class MappingBasisDataIo(DbDataIo):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.mapping_snapshots = []

        self.config = config
        self.current_id_database_table_path = self.config.model_catalog_current_id_table_sde_path
        self.workspace = "in_memory"
        self.class_factory = GenericClassFactory(self.config)
        self.class_factory.class_dict = {"mapping_snapshot": MappingSnapshot,
                                         "mapping_node": MappingNode,
                                         "mapping_link": MappingLink,
                                         "mapping_area": MappingArea}

    #def add_mapping_snapshot(self):
        # use add object - see model catalog db data io for ref

#TODO: add snapshot- add snapshot to db