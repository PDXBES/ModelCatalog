import os
from config import Config
from typing import List
from model import Model
from simulation import Simulation


class ModelDataIO:
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config

    def read_simulations(self, model):
        # type: (Model) -> List[Simulation]
        simulation_descriptions = os.walk(model.simulation_folder_path()).next()[1]
        for simulation_description in simulation_descriptions:
            simulation = Simulation(model.model_path, self.config)
            if simulation_description in self.config.standard_simulation_names():
                simulation_desc_parts = simulation_description.split("-")
                storm_type = simulation_desc_parts[0][0]
                storm_name = simulation_desc_parts[0][1:]
                dev_scenario = ""
                if len(simulation_desc_parts) == 1:
                    dev_scenario = "EX"
                else:
                    dev_scenario = simulation_desc_parts[1]
        pass


