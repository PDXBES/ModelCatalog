from config import Config
from generic_object import GenericObject
from dataio.mapping_basis_data_io import MappingBasisDataIo
from businessclasses.mapping_node import MappingNode
from businessclasses.mapping_area import MappingArea
from businessclasses.mapping_link import MappingLink
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
        self.business_rule = None
        self.mapping_links = []
        self.mapping_nodes = []
        self.mapping_areas = []


    def create_mapping_links(self, mapping_basis_data_io, simulations):
        # type: (self, MappingBasisDataIo) -> List[MappingLink]

        pass

    def create_mapping_nodes(self, mapping_basis_data_io, simulations):
        # type: (self, MappingBasisDataIo) -> List[MappingNode]

        pass

    def create_mapping_areas(self, mapping_basis_data_io, simulations):
        # type: (self, MappingBasisDataIo) -> List[MappingArea]

        pass

