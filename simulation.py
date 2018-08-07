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
        sim_file_path = self.model_path \
                        + "\\" + "sim\\" \
                        + self.storm_id + "-" \
                        + self.dev_scenario_id \
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
