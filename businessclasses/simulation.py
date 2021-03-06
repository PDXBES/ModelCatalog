import os
import arcpy
from config import Config
from generic_object import GenericObject
from collections import OrderedDict
from businessclasses.area_results import AreaResults

try:
    from typing import List, Any
except:
    pass

class Simulation(GenericObject):
    areas = None  # type: List[AreaResults]
    def __init__(self, config):
        # type: (str, Config) -> None
        self.model_path = None
        self.id = None
        self.parent_id = None
        self.dev_scenario_id = None
        self.storm_id = None
        self.sim_desc = ""
        self.config = config
        self.input_field_attribute_lookup = Simulation.input_field_attribute_lookup()
        self.areas = []

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Model_ID"] = "parent_id"
        field_attribute_lookup["Simulation_ID"] = "id"
        field_attribute_lookup["Storm_ID"] = "storm_id"
        field_attribute_lookup["Dev_Scenario_ID"] = "dev_scenario_id"
        field_attribute_lookup["Sim_Desc"] = "sim_desc"
        return field_attribute_lookup

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
            if self.config.storm[self.storm_id][0] in self.config.emgaats_design_storms_with_D:
                sim_file_path = self.model_path \
                           + "\\" + "sim\\" \
                           + self.config.storm[self.storm_id][1] \
                           + self.config.storm[self.storm_id][0] + dev_scenario
            else:
                sim_file_path = self.model_path \
                                + "\\" + "sim\\" \
                                + self.config.storm[self.storm_id][0] + dev_scenario
        return sim_file_path

    def required_for_model_catalog(self, model):
        if (self.storm_id, self.dev_scenario_id) in model.required_storm_and_dev_scenario_ids():
            return True
        else:
            return False

