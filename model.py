import os
import arcpy

try:
    from typing import List, Any
except:
    pass
from simulation import Simulation
from config import Config
from generic_object import GenericObject
from model_alt_bc import ModelAltBC
from model_alt_hydrologic import ModelAltHydrologic
from model_alt_hydraulic import ModelAltHydraulic
from model_alteration import ModelAlteration
from project_type import ProjectType

class Model(GenericObject):

    simulations = None  # type: List[Simulation]

    def __init__(self, config):
        # type: (Config) -> None
        self.id = 0
        self.name = "model"
        self.parent_model_id = 0
        self.model_request_id = 0
        self.project_phase_id = 0
        self.engine_type_id = 0
        self.create_date = None
        self.deploy_date = None
        self.run_date = None
        self.extract_date = None
        self.created_by = None
        self.model_path = None
        self.model_purpose_id = None
        self.model_calibration_file = None
        self.model_status_id = None
        self.model_alteration_file = None
        self.project_num = None
        self.simulations = []
        self.config = config
        self.project_types = []
        self.model_alterations = []
        self.model_geometry = None
        self.config_file_path = None
        self.gdb_file_path = None
        self.sim_file_path = None
        self.object_data_io = None

    def validate_model_path(self):
        valid_model_path = os.path.exists(self.model_path)
        return valid_model_path

    def validate_config_file(self):
        self.config_file_path = self.model_path + "\\" + "emgaats.config"
        config_file_valid = os.path.isfile(self.config_file_path)
        return config_file_valid

    def validate_gdb(self):
        self.gdb_file_path = self.model_path + "\\" + "EmgaatsModel.gdb"
        gdb_file_valid = os.path.exists(self.gdb_file_path)
        return gdb_file_valid

    def validate_sim(self):
        self.sim_file_path = self.simulation_folder_path()
        sim_folder_valid = os.path.exists(self.sim_file_path)
        return sim_folder_valid

    def simulation_folder_path(self):
        sim_file_path = self.model_path + "\\" + "sim"
        return sim_file_path
#TODO: move dataIO functions to a DataIO class; Validate results.gdb;
    @property
    def valid(self):
        if self.validate_model_path():
            is_model_path_valid = True
        else:
            is_model_path_valid = False

        if self.validate_config_file():
            is_config_file_valid = True
        else:
            is_config_file_valid = False

        if self.validate_gdb():
            is_gdb_valid = True
        else:
            is_gdb_valid = False

        if self.validate_sim():
            is_sim_valid = True
        else:
            is_sim_valid = False

        if not is_model_path_valid or not is_config_file_valid or not is_gdb_valid or not is_sim_valid:
            is_valid = False
        else:
            is_valid = True
        return is_valid

    def model_valid_diagnostic(self):
        if self.validate_model_path():
            arcpy.AddMessage("Model Path is valid: " + self.model_path)
        else:
            arcpy.AddMessage("Model Path is not valid: " + self.model_path)

        if self.validate_config_file():
            arcpy.AddMessage("Config File is valid: " + self.config_file_path)
        else:
            arcpy.AddMessage("Config File is not valid: " + self.config_file_path)

        if self.validate_gdb():
            arcpy.AddMessage("GDB is valid: " + self.gdb_file_path)

        else:
            arcpy.AddMessage("GDB is not valid: " + self.gdb_file_path)

        if self.validate_sim():
            arcpy.AddMessage("Sim folder is valid: " + self.sim_file_path)

        else:
            arcpy.AddMessage("Sim folder is not valid: " + self.sim_file_path)

    def create_model_alt_bc(self, alteration_type):
        model_alt_bc = ModelAltBC.initialize_with_current_id(self.config, self.object_data_io)
        model_alt_bc.model_alteration_type_id = self.config.model_alt_bc_id[alteration_type]
        return model_alt_bc

    def create_model_alt_hydrologic(self, alteration_type):
        model_alt_hydrologic = ModelAltHydrologic.initialize_with_current_id(self.config,self.object_data_io)
        model_alt_hydrologic.model_alteration_type_id = self.config.model_alt_hydrologic_id[alteration_type]
        return model_alt_hydrologic

    def create_model_alt_hydraulic(self, alteration_type):
        model_alt_hydraulic = ModelAltHydraulic.initialize_with_current_id(self.config, self.object_data_io)
        model_alt_hydraulic.model_alteration_type_id = self.config.model_alt_hydraulic_id[alteration_type]
        return model_alt_hydraulic

    def create_model_alterations(self, alteration_types, alteration_category):
        if alteration_types is None:
            pass
        else:
            for alteration_type in alteration_types:
                if alteration_category == "bc":
                    model_alteration = self.create_model_alt_bc(alteration_type[0])
                    self.model_alterations.append(model_alteration)
                elif alteration_category == "hydrologic":
                    model_alteration = self.create_model_alt_hydrologic(alteration_type[0])
                    self.model_alterations.append(model_alteration)
                elif alteration_category == "hydraulic":
                    model_alteration = self.create_model_alt_hydraulic(alteration_type[0])
                    self.model_alterations.append(model_alteration)

    def create_model_alterations_bc(self, alteration_types):
        self.create_model_alterations(alteration_types, "bc")

    def create_model_alterations_hydrologic(self, alteration_types):
        self.create_model_alterations(alteration_types, "hydrologic")

    def create_model_alterations_hydraulic(self, alteration_types):
        self.create_model_alterations(alteration_types, "hydraulic")

    def create_project_type(self, project_type_name):
        # type: (str)->ProjectType
        project_type = ProjectType.initialize_with_current_id(self.config, self.object_data_io)
        project_type.project_type_id = self.config.proj_type_id[project_type_name]
        return project_type

    def create_project_types(self, project_types):
        # type: (str)->None
        for project_type_name in project_types:
            project_type = self.create_project_type(project_type_name)
            self.project_types.append(project_type)

    def create_simulations(self):
        self.simulations = self.object_data_io.read_simulations(self)

    # TODO: Create tests for add_project and add_project_types