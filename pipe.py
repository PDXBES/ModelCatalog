import math
class Pipe():
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


    def _calculate_apw(self):
        if self.asmrecommendedaction.upper() == "SP":
            self.apw = self.apwspot
        elif self.asmrecommendedaction.upper() == "CIPP":
            self.apw = self.apwliner
        elif self.asmrecommendedaction.upper() == "OC":
            self.apw = self.apwwhole
        else:
            raise Exception

    def _calculate_capital_cost(self):
        self.capitalcost = (self.bpw - self.apw) / self.asmrecommendednbcr

    def _is_positive_number(self, input_value):
        try:
            float(input_value)
            if input_value < 0 or math.isnan(input_value):
                return False
        except:
            return False
        return True

    def valid(self):
        if self._is_positive_number(self.apw) and self._is_positive_number(self.bpw) and self._is_positive_number(self.capitalcost):
            self._calculate_apw()
            self._calculate_capital_cost()
            return True
        else:
            return False
