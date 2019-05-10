from mapping_object import MappingObject
from collections import OrderedDict


class MappingNode(MappingObject):

    def __init__(self, config):
        self.node_id = None
        self.node_symbology = None
        self.min_freeboard_ft = None
        self.name = "mapping_node"
        self.input_field_attribute_lookup = MappingNode.input_field_attribute_lookup()
        super(MappingNode, self).__init__(config)

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = MappingNode.rrad_input_field_attribute_lookup()
        field_attribute_lookup.update(MappingObject.mapping_object_field_attribute_lookup())
        field_attribute_lookup["sim_desc"] = "sim_desc"
        return field_attribute_lookup

    @staticmethod
    def rrad_input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Simulation_ID"] = "simulation_id"
        field_attribute_lookup["node_id"] = "node_id"
        field_attribute_lookup["node_symbology"] = "node_symbology"
        field_attribute_lookup["MinFreeboardFt"] = "min_freeboard_ft"
        field_attribute_lookup["Shape@"] = "geometry"
        return field_attribute_lookup



