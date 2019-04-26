from businessclasses.generic_class_factory import GenericClassFactory
from businessclasses.config import Config
from object_data_io import ObjectDataIo
from mapping_basis_db_data_io import MappingBasisDbDataIo

class MappingSnapshotDataIo(ObjectDataIo):

    def __init__(self, config, mapping_basis_data_io):
        self.config = config
        self.mapping_basis_data_io = mapping_basis_data_io

    def append_mapping_links(self):
        pass

    def append_mapping_nodes(self):
        pass

    def append_mapping_areas(self):
        pass