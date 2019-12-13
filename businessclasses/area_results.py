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
        if self.has_basement == "Y" or self.has_basement == "U":
            return True
        elif self.has_basement == "N":
            return False
        else:
            raise Exception

    def has_sanitary_connection(self):
        if self.san_connect_type != None:
            return True
        elif self.san_connect_type == None:
            return False
        else:
            raise Exception

    def basement_flooding(self):
        if self.area_type == "BLDG" and self.has_sanitary_connection() is True:
            if self.ffe_above_crown() \
                    and self.max_hgl_above_basement_elev() \
                    and self.basement_exists():
                return True
            else:
                return False
        else:
            return False

    def calculate_bsbr(self, simulation):
        if self.basement_flooding() == False:
            self.bsbr = 0
        else:
            storm = self.config.storm[simulation.storm_id][0]
            try:
                self.bsbr = self.storm_bsbr_lookup[storm]
            except:
                #TODO need to check that storm is in list of BSBR storms? Not all storms require BSBR eg Summer 6
                pass









