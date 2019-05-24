try:
    from typing import List, Any
except:
    pass
from rehab_result import RehabResult
from config import Config
from generic_object import GenericObject
import datetime

class Rehab(GenericObject):
    rehab_results = None  # type: List[RehabResult]

    def __init__(self, config):
        # type: (Config) -> None
        self.name = "Rehab"
        self.config = config
        self.id = None
        self.extract_date = None
        self.last_inspection_date = None
        self.purpose = None
        self.rehab_results = []

    @property
    def valid(self):
        if (isinstance(self.id, int) and isinstance(self.extract_date, datetime.datetime)
                and isinstance(self.last_inspection_date, datetime.datetime) and isinstance(self.purpose, str)):
            return True
        return False

    def calculate_apw(self):
        for rehab_result in self.rehab_results:
            rehab_result.calculate_apw()

    def calculate_capital_cost(self):
        for rehab_result in self.rehab_results:
            rehab_result.calculate_capital_cost()

    def create_rehab_results(self, rehab_data_io):
        pass


