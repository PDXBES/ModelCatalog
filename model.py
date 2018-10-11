import os
try:
    from typing import List, Any
except:
    pass
from simulation import Simulation
from config import Config
from generic_object import GenericObject
from model_alteration import ModelAlteration

class Model(GenericObject):

    simulations = None  # type: List[Simulation]

    def __init__(self, config):
        # type: (Config) -> None
        self.id = 0
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

    def validate_model_path(self):
        valid_model_path = os.path.exists(self.model_path)
        return valid_model_path

    def validate_config_file(self):
        config_file_path = self.model_path + "\\" + "emgaats.config"
        config_file_valid = os.path.isfile(config_file_path)
        return config_file_valid

    def validate_gdb(self):
        gdb_file_path = self.model_path + "\\" + "EmgaatsModel.gdb"
        gdb_file_valid = os.path.exists(gdb_file_path)
        return gdb_file_valid

    def validate_sim(self):
        sim_file_path = self.simulation_folder_path()
        sim_folder_valid = os.path.exists(sim_file_path)
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

    def create_model_alteration(self, id, alteration_type):
        model_alteration = ModelAlteration(self.config)
        model_alteration.id = id
        model_alteration.model_alteration_type_id = self.config.model_alteration_id[alteration_type]
        return model_alteration

    def create_model_alterations(self, alteration_types):
        for alteration_type in alteration_types:
            model_alteration = self.create_model_alteration(None, alteration_type)
            self.model_alterations.append(model_alteration)
