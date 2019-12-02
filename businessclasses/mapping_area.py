from mapping_object import MappingObject
from collections import OrderedDict


class MappingArea(MappingObject):

    def __init__(self, config):
        self.area_id = None
        self.area_name = None
        self.bsbr = None
        self.rrad_area_id = None
        self.input_field_attribute_lookup = MappingArea.input_field_attribute_lookup()
        super(MappingArea, self).__init__(config)

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = MappingArea.rrad_input_field_attribute_lookup()
        field_attribute_lookup.update(MappingObject.mapping_object_field_attribute_lookup())
        field_attribute_lookup["sim_desc"] = "sim_desc"

        field_attribute_lookup["rrad_mapping_area_id"] = "id"
        return field_attribute_lookup

    @staticmethod
    def rrad_input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Simulation_ID"] = "simulation_id"
        field_attribute_lookup["Area_ID"] = "area_id"
        field_attribute_lookup["Area_Name"] = "area_name"
        field_attribute_lookup["BSBR"] = "bsbr"
        field_attribute_lookup["Shape@"] = "geometry"
        field_attribute_lookup["rrad_area_id"] = "rrad_area_id"
        return field_attribute_lookup
