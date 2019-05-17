try:
    from typing import List, Any
except:
    pass
from rehab_result import RehabResult
from config import Config
from generic_object import GenericObject
import datetime

class Rehab(GenericObject):
    pipes = None  # type: List[RehabResult]

    def __init__(self, config):
        # type: (Config) -> None
        self.name = "Rehab"
        self.config = config
        self.id = None
        self.extract_date = None
        self.last_inspection_date = None
        self.purpose = None
        self.pipes = []

    @property
    def valid(self):
        if (isinstance(self.id, int) and isinstance(self.extract_date, datetime.datetime)
                and isinstance(self.last_inspection_date, datetime.datetime) and isinstance(self.purpose, str)):
            return True
        return False

    def calculate_apw(self):
        for pipe in self.pipes:
            pipe.calculate_apw()

    def calculate_capital_cost(self):
        for pipe in self.pipes:
            pipe.calculate_capital_cost()

