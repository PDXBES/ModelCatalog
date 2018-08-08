import os
from config import Config

class Simulation:
    def __init__(self, model_path, config):
        # type: (str, Config) -> None
        self.valid = False
        self.model_path = model_path
        self.simulation_id = None
        self.dev_scenario_id = None
        self.storm_id = None
        self.sim_desc = ""
        self.config = config

    def has_results(self):
        dev_scenario=""
        if self.config.dev_scenario[self.dev_scenario_id] != "EX":
            dev_scenario = "-" + self.config.dev_scenario[self.dev_scenario_id]
        sim_file_path = self.model_path \
                        + "\\" + "sim\\"  \
                        + self.config.storm[self.storm_id][1]\
                        + self.config.storm[self.storm_id][0] + dev_scenario \
                        + "\\results.gdb"
        sim_folder_valid = os.path.exists(sim_file_path)
        return sim_folder_valid

# TODO need to deal with simulation path with different scenarios

    def path(self):
        sim_path = self.model_path +\
                   "\\" + "sim\\" +\
                   self.storm_id #+\
                   #"-" +\
                   #self.scenario
                   #TODO ask Arnel about naming convention
        return sim_path
