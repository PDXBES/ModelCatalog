import arcpy
from model_catalog_exception import ModelCatalog_exception, Field_names_length_does_not_match_row_length_exception
try:
    from typing import List, Any
except:
    pass
from model import Model
from config import Config
from data_io import DataIO

class ModelCatalogDataIO(DataIO):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.current_id_database_table_path = self.config.model_catalog_current_id_table_sde_path


    def retrieve_current_model_id(self):
        current_model_id = self.retrieve_current_id("model")
        return current_model_id

    def retrieve_current_simulation_id(self):
        current_simulation_id = self.retrieve_current_id("simulation")
        return current_simulation_id

    def add_model(self, model, field_names):
        # type: (Model, List[str]) -> None
        if not model.valid:
            raise ModelCatalog_exception

        row = [model.model_id,
               model.parent_model_id,
               model.model_request_id,
               model.project_phase_id,
               model.engine_type_id,
               model.create_date,
               model.created_by,
               model.deploy_date,
               model.extract_date,
               model.run_date,
               model.model_path,
               model.model_purpose_id,
               model.model_calibration_file,
               model.model_status_id,
               model.model_alteration_file,
               model.project_num]

        if len(field_names) != len(row):
            raise Field_names_length_does_not_match_row_length_exception

        cursor = arcpy.da.InsertCursor(self.config.model_tracking_sde_path, field_names)

        cursor.insertRow(row)
        del cursor


