try:
    from typing import List, Any
except:
    pass
from pipe import Pipe
from config import Config

class Rehab():
    pipes = None  # type: List[Pipe]

    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.rehab_id = None
        self.extract_date = None
        self.last_inspection_date = None
        self.purpose = None
        self.pipes = []


    def calculate_apw(self):
        for pipe in self.pipes:
            pipe.calculate_apw()

    def calculate_capital_cost(self):
        for pipe in self.pipes:
            pipe.calculate_capital_cost()
