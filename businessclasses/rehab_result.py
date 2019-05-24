import math
from businessclasses.generic_object import GenericObject


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

