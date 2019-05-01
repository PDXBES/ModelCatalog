from config import Config
from generic_object import GenericObject
from businessclasses.mapping_node import MappingNode
from businessclasses.mapping_area import MappingArea
from businessclasses.mapping_link import MappingLink
from collections import OrderedDict

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

#TODO: create input_field_attribute_lookup
    def create_mapping_links(self, mapping_basis_data_io, simulations):
        # type: (self, MappingBasisDataIo) -> List[MappingLink]

        pass

    def create_mapping_nodes(self, mapping_basis_data_io, simulations):
        # type: (self, MappingBasisDataIo) -> List[MappingNode]

        pass

    def create_mapping_areas(self, mapping_basis_data_io, simulations):
        # type: (self, MappingBasisDataIo) -> List[MappingArea]

        pass

    def id_list(self):
        pass