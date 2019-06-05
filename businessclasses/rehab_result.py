import math
from businessclasses.generic_object import GenericObject
from collections import OrderedDict

class RehabResult(GenericObject):
    def __init__(self):
        self.rehab_id = None
        self.compkey = None
        self.bpw = None
        self.usnode = None
        self.dsnode = None
        self.diamwidth = None
        self.length = None
        self.material = None
        self.apw = None
        self.capitalcost = None
        self.lateralcost = None
        self.manholecost = None
        self.asmrecommendednbcr = None
        self.asmrecommendedaction = None
        self.apwspot = None
        self.apwliner = None
        self.apwwhole = None
        self.lateralcount = None
        self.globalid = None
        self.failure_year = None     # "FailureYear",
        self.integer_grade = None    # "grade_h5",
        self.inspection_date = None  # "inspDate"
        self.inspection_year = None
        self.id = None
        self.geometry = None
        self.root_rating = None
        self.input_field_attribute_lookup = RehabResult.input_field_attribute_lookup()
        self.name = "rehab_result"

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["COMPKEY"] = "compkey"
        field_attribute_lookup["BPW"] = "bpw"
        field_attribute_lookup["usnode"] = "usnode"
        field_attribute_lookup["dsnode"] = "dsnode"
        field_attribute_lookup["diamWidth"] = "diamwidth"
        field_attribute_lookup["length"] = "length"
        field_attribute_lookup["material"] = "material"
        field_attribute_lookup["lateralCost"] = "lateralcost"
        field_attribute_lookup["manholeCost"] = "manholecost"
        field_attribute_lookup["ASMRecommendednBCR"] = "asmrecommendednbcr"
        field_attribute_lookup["ASMRecommendedAction"] = "asmrecommendedaction",
        field_attribute_lookup["APWspot"] = "apwspot"
        field_attribute_lookup["APWLiner"] = "apwliner"
        field_attribute_lookup["APWWhole"] = "apwwhole"
        field_attribute_lookup["lateralCOUNT"] = "lateralcount"
        field_attribute_lookup["GLOBALID"] = "globalid"
        field_attribute_lookup["FailureYear"] = "failure_year"
        field_attribute_lookup["Integer_Condition_Grade"] = "integer_grade"
        field_attribute_lookup["Last_Inspection_Date"] = "inspection_date"
        field_attribute_lookup["APW"] = "apw"
        field_attribute_lookup["capitalCost"] = "capitalcost"
        field_attribute_lookup["Rehab_ID"] = "rehab_id"
        field_attribute_lookup["rrad_rehab_result_id"] = "id"
        field_attribute_lookup["shape@"] = "geometry"
        field_attribute_lookup["ROOT_RATING"] = "root_rating"
        return field_attribute_lookup

    @staticmethod
    def nbcr_data_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["compkey"] = "compkey"
        field_attribute_lookup["usnode"] = "usnode"
        field_attribute_lookup["dsnode"] = "dsnode"
        field_attribute_lookup["diamWidth"] = "diamwidth"
        field_attribute_lookup["length"] = "length"
        field_attribute_lookup["material"] = "material"
        field_attribute_lookup["lateralCost"] ="lateralcost"
        field_attribute_lookup["manholeCost"] = "manholecost"
        field_attribute_lookup["ASMRecommendednBCR"] ="asmrecommendednbcr"
        field_attribute_lookup["ASMRecommendedAction"] = "asmrecommendedaction"
        field_attribute_lookup["APWSpot"] = "apwspot"
        field_attribute_lookup["APWLiner"] = "apwliner"
        field_attribute_lookup["APWWhole"] = "apwwhole"
        field_attribute_lookup["lateralCount"] = "lateralcount"
        field_attribute_lookup["GLOBALID"] = "globalid"
        field_attribute_lookup["FailureYear"] = "failure_year"
        field_attribute_lookup["grade_h5"] = "integer_grade"
        field_attribute_lookup["inspDate"] = "inspection_date"
        field_attribute_lookup["shape@"] = "geometry"
        return field_attribute_lookup

    @staticmethod
    def rehab_branches_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["BPW"] = "bpw"
        field_attribute_lookup["compkey"] = "compkey"
        return field_attribute_lookup

    @staticmethod
    def tv_ratings_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["ROOT_RATING"] = "root_rating"
        field_attribute_lookup["GLOBALID"] = "global_id"
        return field_attribute_lookup

    def calculate_apw(self):
        if self.asmrecommendedaction.upper() == "SP":
            self.apw = self.apwspot
        elif self.asmrecommendedaction.upper() == "CIPP":
            self.apw = self.apwliner
        elif self.asmrecommendedaction.upper() == "OC":
            self.apw = self.apwwhole
        else:
            #TODO not sure what to do with this exception
            #raise Exception
            pass

    def calculate_capital_cost(self):
        if self._is_greater_than_zero(self.apw) and self._is_greater_than_zero(self.asmrecommendednbcr):
            self.capitalcost = (self.bpw - self.apw) / self.asmrecommendednbcr
        else:
            return None

    def _is_greater_than_zero(self, input_value):
        try:
            float(input_value)
            if input_value <= 0 or math.isnan(input_value):
                return False
        except:
            return False
        return True

    def valid(self):
        #TODO we need the BPW for all pipes so we need to decide what a valid pipe really should be
        if self._is_greater_than_zero(self.apw) and self._is_greater_than_zero(self.bpw) and self._is_greater_than_zero(self.capitalcost):
            return True
        else:
            return False

