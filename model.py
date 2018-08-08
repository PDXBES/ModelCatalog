import os

from typing import List, Any
from simulation import Simulation
from config import Config


class Model:

    simulations = None  # type: List[Simulation]

    def __init__(self, config):
        # type: (Config) -> None
        self.model_id = 0
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
        self.project_type_id = None
        self.model_purpose_id = None
        self.model_calibration_file = None
        self.model_status_id = None
        self.model_alterations_id = None
        self.model_alteration_file = None
        self.project_num = None
        self.simulations = []
        self.config = config

# TODO - correct capitalization of attributes to PEP8 (lower)

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
        sim_file_path = self.model_path + "\\" + "sim"
        sim_folder_valid = os.path.exists(sim_file_path)
        return sim_folder_valid

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
