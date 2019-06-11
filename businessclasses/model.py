import os
import arcpy
from simulation import Simulation
from config import Config
from generic_object import GenericObject
from model_alt_bc import ModelAltBc
from model_alt_hydrologic import ModelAltHydrologic
from model_alt_hydraulic import ModelAltHydraulic
from model_alteration import ModelAlteration
from project_type import ProjectType
from collections import OrderedDict
import datetime
from model_catalog_exception import InvalidCalibrationStormSimulationDescription
from model_catalog_exception import InvalidModelPurpose
from model_catalog_exception import InvalidProjectPhase
try:
    from typing import List, Any
except:
    pass


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
        self.input_field_attribute_lookup = Model.input_field_attribute_lookup()
        self.parent_model_path = None
        self.parent_model_registration_file_path = None

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Model_ID"] = "id"
        field_attribute_lookup["Parent_Model_ID"] = "parent_model_id"
        field_attribute_lookup["Model_Request_ID"] = "model_request_id"
        field_attribute_lookup["Project_Phase_ID"] = "project_phase_id"
        field_attribute_lookup["Engine_Type_ID"] = "engine_type_id"
        field_attribute_lookup["Create_Date"] = "create_date"
        field_attribute_lookup["Created_by"] = "created_by"
        field_attribute_lookup["Deploy_Date"] = "deploy_date"
        field_attribute_lookup["Extract_Date"] = "extract_date"
        field_attribute_lookup["Run_Date"] = "run_date"
        field_attribute_lookup["Model_Path"] = "model_path"
        field_attribute_lookup["Model_Purpose_ID"] = "model_purpose_id"
        field_attribute_lookup["Model_Calibration_file"] = "model_calibration_file"
        field_attribute_lookup["Model_Status_ID"] = "model_status_id"
        field_attribute_lookup["Model_Alteration_file"] = "model_alteration_file"
        field_attribute_lookup["Project_Num"] = "project_num"
        field_attribute_lookup["Shape@"] = "model_geometry"
        return field_attribute_lookup

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
        if self.config.model_status[self.model_status_id] == "Working":
            if self.valid_emgaats_model_structure():
                return True
        elif self.config.model_status[self.model_status_id] == "Final":
            if self.project_phase_id == self.config.proj_phase_id["Pre Design"] or \
                    self.project_phase_id == self.config.proj_phase_id["Design 30"] or \
                    self.project_phase_id == self.config.proj_phase_id["Design 60"] or \
                    self.project_phase_id == self.config.proj_phase_id["Design 90"]:
                if self.valid_emgaats_model_structure():
                    return True
            elif self.project_phase_id == self.config.proj_phase_id["Planning"]:
                if self.model_purpose_id == self.config.model_purpose_id["Calibration"]:
                    if self.valid_emgaats_model_structure() and self.valid_calibration_simulations():
                        return True
                elif self.model_purpose_id == self.config.model_purpose_id["Characterization"]:
                    if self.valid_emgaats_model_structure() and self.valid_required_simulations():
                        return True
                elif self.model_purpose_id == self.config.model_purpose_id["Alternative"]:
                    if self.valid_emgaats_model_structure() and self.valid_required_simulations():
                        return True
                elif self.model_purpose_id == self.config.model_purpose_id["Recommended Plan"]:
                    if self.valid_emgaats_model_structure() and self.valid_required_simulations():
                        return True
            return False
    #TODO: will need to add check for registration_file.json if model is not calibration

    def valid_emgaats_model_structure(self):
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

    def valid_calibration_simulations(self):
        for simulation in self.simulations:
            if simulation.storm_id == 0:
                if len(simulation.sim_desc) == 11:
                    try:
                        sim_year = int(simulation.sim_desc[3:7])
                        sim_month = int(simulation.sim_desc[7:9])
                        sim_day = int(simulation.sim_desc[9:11])
                        current_date = datetime.datetime.now()
                        simulation_date = datetime.datetime(year=sim_year, month=sim_month, day=sim_day)
                        if simulation_date < current_date:
                            return True
                    except:
                        raise InvalidCalibrationStormSimulationDescription()
        return False

    def valid_required_simulations(self):
        required_storm_and_dev_scenario_ids = self.required_storm_and_dev_scenario_ids()

        for required_storm_id, required_dev_scenario in required_storm_and_dev_scenario_ids:
            required_simulation_found = False
            for simulation in self.simulations:
                if required_storm_id == simulation.storm_id and required_dev_scenario == simulation.dev_scenario_id:
                    required_simulation_found = True
            if required_simulation_found == False:
                return False
        return True

    def required_storm_and_dev_scenario_ids(self):
        if self.project_phase_id == self.config.proj_phase_id["Planning"]:
            if self.model_purpose_id == self.config.model_purpose_id["Characterization"]:
                required_storm_and_dev_scenario_ids = self.config.ccsp_characterization_storm_and_dev_scenario_ids
            elif self.model_purpose_id == self.config.model_purpose_id["Alternative"]:
                required_storm_and_dev_scenario_ids = self.config.ccsp_alternative_storm_and_dev_scenario_ids
            elif self.model_purpose_id == self.config.model_purpose_id["Recommended Plan"]:
                required_storm_and_dev_scenario_ids = self.config.ccsp_recommended_plan_storm_and_dev_scenario_ids
            else:
                raise InvalidModelPurpose
        else:
            raise InvalidProjectPhase
        return required_storm_and_dev_scenario_ids

    def model_valid_diagnostic(self):
        self.valid_emgaats_model_structure_diagnostic()

    def valid_emgaats_model_structure_diagnostic(self):
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

    def create_model_alt_bc(self, alteration_type, modelcatalog_db_data_io):
        model_alt_bc = ModelAltBc.initialize_with_current_id(self.config, modelcatalog_db_data_io)
        model_alt_bc.model_alteration_type_id = self.config.model_alt_bc_id[alteration_type]
        return model_alt_bc

    def create_model_alt_hydrologic(self, alteration_type, modelcatalog_db_data_io):
        model_alt_hydrologic = ModelAltHydrologic.initialize_with_current_id(self.config, modelcatalog_db_data_io)
        model_alt_hydrologic.model_alteration_type_id = self.config.model_alt_hydrologic_id[alteration_type]
        return model_alt_hydrologic

    def create_model_alt_hydraulic(self, alteration_type, modelcatalog_db_data_io):
        model_alt_hydraulic = ModelAltHydraulic.initialize_with_current_id(self.config, modelcatalog_db_data_io)
        model_alt_hydraulic.model_alteration_type_id = self.config.model_alt_hydraulic_id[alteration_type]
        return model_alt_hydraulic

    def create_model_alterations(self, alteration_types, alteration_category, modelcatalog_db_data_io):
        if alteration_types is None:
            pass
        else:
            for alteration_type in alteration_types:
                if alteration_category == "bc":
                    model_alteration = self.create_model_alt_bc(alteration_type[0], modelcatalog_db_data_io)
                    self.model_alterations.append(model_alteration)
                elif alteration_category == "hydrologic":
                    model_alteration = self.create_model_alt_hydrologic(alteration_type[0], modelcatalog_db_data_io)
                    self.model_alterations.append(model_alteration)
                elif alteration_category == "hydraulic":
                    model_alteration = self.create_model_alt_hydraulic(alteration_type[0], modelcatalog_db_data_io)
                    self.model_alterations.append(model_alteration)

    def create_model_alterations_bc(self, alteration_types, modelcatalog_db_data_io):
        self.create_model_alterations(alteration_types, "bc", modelcatalog_db_data_io)

    def create_model_alterations_hydrologic(self, alteration_types, modelcatalog_db_data_io):
        self.create_model_alterations(alteration_types, "hydrologic", modelcatalog_db_data_io)

    def create_model_alterations_hydraulic(self, alteration_types, modelcatalog_db_data_io):
        self.create_model_alterations(alteration_types, "hydraulic", modelcatalog_db_data_io)

    def create_project_type(self, project_type_name, modelcatalog_db_data_io):
        # type: (str)->ProjectType
        project_type = ProjectType.initialize_with_current_id(self.config, modelcatalog_db_data_io)
        project_type.project_type_id = self.config.proj_type_id[project_type_name]
        project_type.parent_id = self.id
        return project_type

    def create_project_types(self, project_types, modelcatalog_db_data_io):
        # type: (str)->None
        for project_type_name in project_types:
            project_type = self.create_project_type(project_type_name, modelcatalog_db_data_io)
            self.project_types.append(project_type)

    def create_simulations(self, model_data_io):
        self.simulations = model_data_io.read_simulations(self)

    # TODO: Create tests for add_project and add_project_types

    def ready_to_register(self):
        if self.config.model_status[self.model_status_id] == "Working":
            return self.valid
        return False
    #Todo : change this to call a diagnostic method

    def write_to_rrad(self):
        if self.valid:
            if self.model_status_id == self.config.model_status_id["Final"]:
                if self.project_phase_id == self.config.proj_phase_id["Planning"]:
                    if self.model_purpose_id != self.config.model_purpose_id["Calibration"]:
                        return True
        return False


    def validate_registration(self):
        self.parent_model_registration_file_path = self.parent_model_path + "\\" + "registration_file.json"
        parent_model_registration_file_valid = os.path.isfile(self.parent_model_registration_file_path)
        return parent_model_registration_file_valid


