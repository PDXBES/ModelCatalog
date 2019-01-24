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
        self.input_field_attribute_lookup = None
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
        self.input_field_attribute_lookup = Area.input_field_attribute_lookup()
        self.geometry = None
        self.bsbr = None
        self.basement_depth = 8
        self.storm_bsbr_lookup = {"2yr6h": 91535, "5yr6h": 36614, "25yr6h": 7323}

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
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

    @staticmethod
    def output_field_attribute_lookup():
        output_field_attribute_lookup = Area.input_field_attribute_lookup()
        for key, value in Area.field_attribute_lookup_required_for_output().items():
            output_field_attribute_lookup[key] = value

        return output_field_attribute_lookup

    @staticmethod
    def field_attribute_lookup_required_for_output():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Simulation_ID"] = "parent_id"
        field_attribute_lookup["bsbr"] = "bsbr"
        return field_attribute_lookup




    #def determine_area_type(self):

    # check if basement higher than crown

    def ffe_above_crown(self):
        try:
            elev_diff = self.first_floor_elev_ft - self.san_crown_elev_ft
        except:
            pass
        return elev_diff >= self.basement_depth

    def max_hgl_above_basement_elev(self):

        return self.first_floor_elev_ft - self.maxHGL < self.basement_depth

    def basement_exists(self):
        if self.has_basement is "Y" or self.has_basement is "U":
            return True
        elif self.has_basement is "N":
            return False
        else:
            raise Exception

    def basement_flooding(self):
        if self.area_type is "BLDG":
            if self.ffe_above_crown() \
                    and self.max_hgl_above_basement_elev() \
                    and self.basement_exists():
                return True
            else:
                return False
        else:
            return False


    def calculate_bsbr(self, simulation):
        if self.basement_flooding() is False:
            self.bsbr = 0
        else:
            storm = self.config.storm[simulation.storm_id][0]
            self.bsbr = self.storm_bsbr_lookup[storm]









