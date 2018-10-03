import arcpy
from model_catalog_exception import ModelCatalog_exception, Field_names_length_does_not_match_row_length_exception
try:
    from typing import List, Any
except:
    pass
from model import Model
from config import Config
from data_io import DataIO
from collections import OrderedDict

class ModelCatalogDataIO(DataIO):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.current_id_database_table_path = self.config.model_catalog_current_id_table_sde_path
        self.field_attribute_lookup = OrderedDict()
        self.field_attribute_lookup["Model_ID"] = "model_id"
        self.field_attribute_lookup["Parent_Model_ID"] = "parent_model_id"
        self.field_attribute_lookup["Model_Request_ID"] = "model_request_id"
        self.field_attribute_lookup["Project_Phase_ID"] = "project_phase_id"
        self.field_attribute_lookup["Engine_Type_ID"] = "engine_type_id"
        self.field_attribute_lookup["Create_Date"] = "create_date"
        self.field_attribute_lookup["Created_by"] = "created_by"
        self.field_attribute_lookup["Deploy_Date"] = "deploy_date"
        self.field_attribute_lookup["Extract_Date"] = "extract_date"
        self.field_attribute_lookup["Run_Date"] = "run_date"
        self.field_attribute_lookup["Model_Path"] = "model_path"
        self.field_attribute_lookup["Model_Purpose_ID"] = "model_purpose_id"
        self.field_attribute_lookup["Model_Calibration_file"] = "model_calibration_file"
        self.field_attribute_lookup["Model_Status_ID"] = "model_status_id"
        self.field_attribute_lookup["Model_Alteration_file"] = "model_alteration_file"
        self.field_attribute_lookup["Project_Num"] = "project_num"
        self.field_attribute_lookup["Shape@"] = "model_geometry"

    def retrieve_current_model_id(self):
        current_model_id = self.retrieve_current_id("model")
        return current_model_id

    def retrieve_current_simulation_id(self):
        current_simulation_id = self.retrieve_current_id("simulation")
        return current_simulation_id

    def add_model(self, model):
        # type: (Model) -> None
        self.add_object(model)


