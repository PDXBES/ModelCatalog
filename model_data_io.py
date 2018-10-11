import os
import arcpy
from config import Config
try:
    from typing import List, Any
except:
    pass
from model import Model
from simulation import Simulation
from model_catalog_data_io import ModelCatalogDataIO
from model_catalog_exception import Invalid_Model_exception
from data_io import DataIO

class ModelDataIO(DataIO):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
    def create_model_geometry(self, model):
        if model.valid:
            model_name = "Links"
            model_in = model.model_path + "\\" + "EmgaatsModel.gdb" + "\\Network\\" + model_name
            model_out = "in_memory\\" + model_name
            arcpy.Dissolve_management(model_in, model_out, "", "", "MULTI_PART")
            cursor = arcpy.da.SearchCursor(model_out, ["Shape@"])
            for row in cursor:
                geometry = row[0]
                model.model_geometry = geometry
            del cursor
            arcpy.Delete_management(model_out)
        else:
            raise Invalid_Model_exception

    def read_simulations(self, model):
        # type: (Model) -> List[Simulation]
        simulations = []  # type: List[Simulation]
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
            else:
                dev_scenario = "EX"
                storm_type = "U"
                storm_name = "user_def"
            simulation.storm_id = self.config.storm_id[(storm_name, storm_type)]
            simulation.dev_scenario_id = self.config.dev_scenario_id[dev_scenario]
            simulation.sim_desc = simulation_description
            simulations.append(simulation)
        return simulations

    def add_simulation(self, model_id, simulation, model_catalog_data_io):
        # type: (int, Simulation, ModelCatalogDataIO) -> None
        field_names = ["Model_ID", "Simulation_ID", "Storm_ID", "Dev_Scenario_ID", "Sim_Desc"]
        simulation.simulation_id = model_catalog_data_io.retrieve_current_simulation_id()

        row = [model_id,
               simulation.simulation_id,
               simulation.storm_id,
               simulation.dev_scenario_id,
               simulation.sim_desc]

        cursor = arcpy.da.InsertCursor(self.config.simulation_sde_path, field_names)

        cursor.insertRow(row)
        del cursor

    def add_simulations(self, model, model_catalog_data_io):
        # type: (Model, ModelCatalogDataIO) -> None

        for simulation in model.simulations:
            self.add_simulation(model.id, simulation, model_catalog_data_io)

    def add_model_alteration(self, model_alteration):
        # type: (ModelAlteration) -> None

        self.add_object(model_alteration, self.field_attribute_lookup, self.config.model_tracking_sde_path)







