import os
import arcpy
from businessclasses.config import Config
try:
    from typing import List, Any
except:
    pass
from businessclasses.model import Model
from businessclasses.simulation import Simulation
from businessclasses.model_catalog_exception import InvalidModelException
from db_data_io import DbDataIo
from object_data_io import ObjectDataIo
from businessclasses.model_alteration import ModelAlteration
from businessclasses.project_type import ProjectType

class ModelDataIo(ObjectDataIo):
    def __init__(self, config, db_data_io):
        # type: (Config, DbDataIo) -> None
        self.config = config
        self.db_data_io = db_data_io

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
            raise InvalidModelException

    def read_simulations(self, model):
        # type: (Model) -> List[Simulation]
        simulations = []  # type: List[Simulation]
        simulation_descriptions = os.walk(model.simulation_folder_path()).next()[1]
        for simulation_description in simulation_descriptions:
            simulation = Simulation.initialize_with_current_id(self.config, model.object_data_io)
            simulation.model_path = model.model_path
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
                storm_name = "User-defined"
            simulation.storm_id = self.config.storm_id[(storm_name, storm_type)]
            simulation.dev_scenario_id = self.config.dev_scenario_id[dev_scenario]
            simulation.sim_desc = simulation_description
            simulations.append(simulation)
        return simulations

    def add_simulation(self, model_id, simulation):
        # type: (int, Simulation) -> None
        self.add_object(model_id, simulation, simulation.input_field_attribute_lookup, self.config.simulation_sde_path)


    def add_simulations(self, model):
        # type: (Model) -> None
        for simulation in model.simulations:
            self.add_simulation(model.id, simulation)

    def add_model_alteration(self, model_id, model_alteration):
        # type: (int, ModelAlteration) -> None
        if model_alteration.name == "model_alt_bc":
            self.add_object(model_id, model_alteration, model_alteration.input_field_attribute_lookup, self.config.model_alt_bc_sde_path)
        elif model_alteration.name == "model_alt_hydrologic":
            self.add_object(model_id, model_alteration, model_alteration.input_field_attribute_lookup, self.config.model_alt_hydrologic_sde_path)
        elif model_alteration.name == "model_alt_hydraulic":
            self.add_object(model_id, model_alteration, model_alteration.input_field_attribute_lookup, self.config.model_alt_hydraulic_sde_path)

    def add_model_alterations(self, model):
        # type: (Model) -> None
        for model_alteration in model.model_alterations:
            self.add_model_alteration(model.id, model_alteration)

    def add_project_type(self, model_id, project_type):
        # type: (int, ProjectType) -> None
        self.add_object(model_id, project_type, project_type.input_field_attribute_lookup,
                        self.config.project_type_sde_path)

    def add_project_types(self, model):
        # type: (Model) -> None
        for project_type in model.project_types:
            self.add_project_type(model.id, project_type)

# TODO: finish the below functions
    def read_extraction_date_from_emgaats_config_file(self):
        pass

    # get list of emgaats data for all models in the folder
    #use brents existing xml notes
    # will return the list

    def read_deploy_date_and_results_extracted_date_from_emgaats_config_file(self):
        pass
    #get list of emgaats data for all simulations in the folder
    #will return the list
    #awaiting changes from Arnel









