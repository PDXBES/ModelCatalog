import arcpy
import os
from model_catalog_exception import ModelCatalog_exception, Field_names_length_does_not_match_row_length_exception
from typing import List, Any
from model import Model
from config import Config

class ModelCatalogDataIO():
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config


    def retrieve_next_model_id(self, location, field_names):
        cursor = arcpy.da.UpdateCursor(location, field_names)
        object_name, current_id = cursor.next()
        next_id = current_id + 1
        cursor.updateRow([object_name, next_id])
        return current_id

    def add_model(self, model, location, field_names):
        # type: (Model, str, List[str]) -> None
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
               model.project_type_id,
               model.model_purpose_id,
               model.model_calibration_file,
               model.model_status_id,
               model.model_alterations_id,
               model.model_alteration_file,
               model.project_num]

        if len(field_names) != len(row):
            raise Field_names_length_does_not_match_row_length_exception

        cursor = arcpy.da.InsertCursor(location, field_names)

        cursor.insertRow(row)
        del cursor

    def storm_scenario_dict(self, location):
        list_of_domains = arcpy.da.ListDomains(location)
        dict_of_scenarios = None
        for domain in list_of_domains:
            if domain.name == "Dev_Scenario":
                dict_of_scenarios = domain.codedValues
                break
        return dict_of_scenarios

