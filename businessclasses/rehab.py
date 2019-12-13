try:
    from typing import List, Any
except:
    pass
from rehab_result import RehabResult
from config import Config
from generic_object import GenericObject
import datetime
from collections import OrderedDict


class Rehab(GenericObject):
    rehab_results = None  # type: List[RehabResult]

    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.id = None
        self.extract_date = None
        self.last_inspection_date = None
        self.purpose = None
        self.rehab_results = []

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Rehab_ID"] = "id"
        field_attribute_lookup["Extract_Date"] = "extract_date"
        field_attribute_lookup["Last_Inspection_Date"] = "last_inspection_date"
        field_attribute_lookup["Purpose"] = "purpose"
        return field_attribute_lookup

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
        rehab_result = RehabResult(self.config)
        rehab_results_table_name = "rehab_results_table_name"
        rehab_results_table = rehab_data_io.rrad_db_data_io.workspace + "\\" + "rehab_results_table_name"
        rehab_data_io.copy_rehab_results_to_memory(rehab_results_table_name, self)
        self.rehab_results = rehab_data_io.rrad_db_data_io.create_objects_from_table_with_current_id(RehabResult,
                                                                                                     rehab_results_table,
                                                                                                     rehab_result.rehab_result_field_attribute_lookup())

        self.calculate_apw()
        self.calculate_capital_cost()

        # delete in memory - need fully qualified name


