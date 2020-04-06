from generic_object import GenericObject
from collections import OrderedDict
from config import Config
try:
    from typing import List, Any
except:
    pass

class AreaResults(GenericObject):


    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.object_data_io = None
        self.parent_id = None
        self.input_field_attribute_lookup = None
        self.id = None
        self.area_id = None
        self.name = "area"
        self.area_name = None
        self.first_floor_elev_ft = None
        self.first_floor_elev_qc = None
        self.has_basement = None
        self.has_basement_qc = None
        self.minDHGL = None
        self.maxHGL = None
        self.san_crown_elev_ft = None
        self.area_type = None
        self.input_field_attribute_lookup = AreaResults.results_field_attribute_lookup()
        self.geometry = None
        self.bsbr = None
        self.basement_depth = 8
        self.storm_bsbr_lookup = {"02yr6h": 91535, "05yr6h": 36614, "10yr6h": 18307, "25yr6h": 7323}
        self.san_connect_type = None

    @staticmethod
    def results_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["area_id"] = "area_id"
        field_attribute_lookup["area_name"] = "area_name"
        field_attribute_lookup["first_floor_elev_ft"] = "first_floor_elev_ft"
        field_attribute_lookup["first_floor_elev_qc"] = "first_floor_elev_qc"
        field_attribute_lookup["has_basement"] = "has_basement"
        field_attribute_lookup["has_basement_qc"] = "has_basement_qc"
        field_attribute_lookup["minDHGL"] = "minDHGL"
        field_attribute_lookup["maxHGL"] = "maxHGL"
        field_attribute_lookup["san_crown_elev_ft"] = "san_crown_elev_ft"
        field_attribute_lookup["area_type"] = "area_type"
        field_attribute_lookup["san_connect_type"] = "san_connect_type"
        return field_attribute_lookup

    @staticmethod
    def input_field_attribute_lookup():
        output_field_attribute_lookup = AreaResults.results_field_attribute_lookup()
        output_field_attribute_lookup["Simulation_ID"] = "parent_id"
        output_field_attribute_lookup["bsbr"] = "bsbr"
        output_field_attribute_lookup["rrad_area_id"] = "id"
        return output_field_attribute_lookup


    #def determine_area_type(self):










