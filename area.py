from generic_object import GenericObject
from collections import OrderedDict
from config import Config
try:
    from typing import List, Any
except:
    pass

class Area(GenericObject):


    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.object_data_io = None
        self.parent_id = None
        self.field_attribute_lookup = None
        self.id = None
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
        self.field_attribute_lookup = Area.field_attribute_lookup()
        self.geometry = None

    @staticmethod
    def field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        #field_attribute_lookup["Simulation_ID"] = "parent_id"
        field_attribute_lookup["area_id"] = "id"
        field_attribute_lookup["area_name"] = "area_name"
        field_attribute_lookup["first_floor_elev_ft"] = "first_floor_elev_ft"
        field_attribute_lookup["first_floor_elev_qc"] = "first_floor_elev_qc"
        field_attribute_lookup["has_basement"] = "has_basement"
        field_attribute_lookup["has_basement_qc"] = "has_basement_qc"
        field_attribute_lookup["minDHGL"] = "minDHGL"
        field_attribute_lookup["maxHGL"] = "maxHGL"
        field_attribute_lookup["san_crown_elev_ft"] = "san_crown_elev_ft"
        field_attribute_lookup["area_type"] = "area_type"
        field_attribute_lookup["Shape@"] = "geometry"

        return field_attribute_lookup

    #def determine_area_type(self):

    # check if basement higher than crown

    def determine_basement_flooding(self):
        pass












