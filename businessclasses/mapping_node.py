from mapping_object import MappingObject
from collections import OrderedDict


class MappingNode(MappingObject):

    def __init__(self):
        self.global_id = None
        self.node_symbology = None
        self.min_freeboard_ft = None
        self.input_field_attribute_lookup = MappingNode.input_field_attribute_lookup()

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = MappingNode.rrad_input_field_attribute_lookup()
        field_attribute_lookup.update(MappingObject.mapping_object_field_attribute_lookup())
        return field_attribute_lookup

    @staticmethod
    def rrad_input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Global_ID"] = "global_id"
        field_attribute_lookup["Node_Symbology"] = "node_symbology"
        field_attribute_lookup["Min_Freeboard_Ft"] = "min_freeboard_ft"
        return field_attribute_lookup



