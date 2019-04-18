from mapping_object import MappingObject
from collections import OrderedDict


class MappingArea(MappingObject):

    def __init__(self):
        self.area_id = None
        self.area_name = None

        self.bsbr = None

        self.input_field_attribute_lookup = MappingArea.input_field_attribute_lookup()

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Area_ID"] = "area_id"
        field_attribute_lookup["Area_Name"] = "area_name"
        field_attribute_lookup["BSBR"] = "bsbr"
        field_attribute_lookup.update(MappingObject.mapping_object_field_attribute_lookup())
        return field_attribute_lookup
