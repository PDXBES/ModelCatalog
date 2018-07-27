import os

class Simulation:
    def __init__(self, model_path):
        self.storm = ""
        self.scenario = ""
        self.valid = False
        self.model_path = model_path

    def has_results(self):
        sim_file_path = self.model_path \
                        + "\\" + "sim\\" \
                        + self.storm + "-" \
                        + self.scenario \
                        + "\\results.gdb"
        sim_folder_valid = os.path.exists(sim_file_path)
        return sim_folder_valid

    def path(self):
        sim_path = self.model_path +\
                   "\\" + "sim\\" +\
                   self.storm +\
                   "-" +\
                   self.scenario
        return sim_path