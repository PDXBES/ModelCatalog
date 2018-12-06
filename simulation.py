import os
from config import Config
from generic_object import GenericObject
from collections import OrderedDict
from area import Area
from db_data_io import DbDataIo

try:
    from typing import List, Any
except:
    pass

class Simulation(GenericObject):
    areas = None  # type: List[Area]
    def __init__(self, config):
        # type: (str, Config) -> None
        self.model_path = None
        self.id = None
        self.parent_id = None
        self.name = "simulation"
        self.dev_scenario_id = None
        self.storm_id = None
        self.sim_desc = ""
        self.config = config
        self.field_attribute_lookup = OrderedDict()
        self.field_attribute_lookup["Model_ID"] = "parent_id"
        self.field_attribute_lookup["Simulation_ID"] = "id"
        self.field_attribute_lookup["Storm_ID"] = "storm_id"
        self.field_attribute_lookup["Dev_Scenario_ID"] = "dev_scenario_id"
        self.field_attribute_lookup["Sim_Desc"] = "sim_desc"
        self.areas = []

    def valid(self):
        return self.has_results()

    def has_results(self):
        sim_file_path = self.path()
        sim_folder_valid = os.path.exists(sim_file_path)
        return sim_folder_valid

    def path(self):
        dev_scenario = ""
        if self.config.dev_scenario[self.dev_scenario_id] != "EX":
            dev_scenario = "-" + self.config.dev_scenario[self.dev_scenario_id]
        if self.storm_id == 0:
            sim_file_path = self.model_path + "\\" + "sim\\" + self.sim_desc
        else:
            sim_file_path = self.model_path \
                       + "\\" + "sim\\" \
                       + self.config.storm[self.storm_id][1] \
                       + self.config.storm[self.storm_id][0] + dev_scenario
        return sim_file_path

    def create_areas(self, input_table, db_data_io):
        area = Area(self.config)
        db_data_io.create_objects_from_table(input_table, "area", area.field_attribute_lookup)

