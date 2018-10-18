import os
from config import Config
from generic_object import GenericObject
from collections import OrderedDict

class Simulation(GenericObject):
    def __init__(self, model_path, config):
        # type: (str, Config) -> None
        self.valid = False
        self.model_path = model_path
        self.id = None
        self.dev_scenario_id = None
        self.storm_id = None
        self.sim_desc = ""
        self.config = config
        self.field_attribute_lookup = OrderedDict()
        self.field_attribute_lookup[0] = ["Model_ID", "parent_id"]
        self.field_attribute_lookup[1] = ["Simulation_ID", "id"]
        self.field_attribute_lookup[2] = ["Storm_ID", "storm_id"]
        self.field_attribute_lookup[3] = ["Dev_Scenario_ID", "dev_scenario_id"]
        self.field_attribute_lookup[4] = ["Sim_Desc", "sim_desc"]

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

