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


    def calculate_apw(self):
        if self.asmrecommendedaction.upper() == "SP":
            self.apw = self.apwspot
        elif self.asmrecommendedaction.upper() == "CIPP":
            self.apw = self.apwliner
        elif self.asmrecommendedaction.upper() == "OC":
            self.apw = self.apwwhole
        else:
            raise Exception

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
        if self._is_greater_than_zero(self.apw) and self._is_greater_than_zero(self.bpw) and self._is_greater_than_zero(self.capitalcost):
            return True
        else:
            return False

