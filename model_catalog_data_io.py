import arcpy
from model_catalog_exception import ModelCatalog_exception, Field_names_length_does_not_match_row_length_exception
from typing import List, Any
from model import Model
from config import Config

class ModelCatalogDataIO():
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config

    def retrieve_current_id(self, object_type):
        # type: (str, str) -> int
        field_names = ["Object_Type", "Current_ID"]
        cursor = arcpy.da.UpdateCursor(self.config.current_id_table_sde_path, field_names)
        for row in cursor:
            object_name, current_id = row
            if object_type == object_name:
                next_id = current_id + 1
                break
        cursor.updateRow([object_name, next_id])
        return current_id

    def retrieve_current_model_id(self):
        current_model_id = self.retrieve_current_id("model")
        return current_model_id

    def retrieve_current_simulation_id(self):
        current_simulation_id = self.retrieve_current_id("simulation")
        return current_simulation_id

    def add_model(self, model, field_names):
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

        cursor = arcpy.da.InsertCursor(self.config.model_tracking_sde_path, field_names)

        cursor.insertRow(row)
        del cursor

    @staticmethod
    def retrieve_domain_as_dict(domain_name, model_catalog_path_sde):
        list_of_domains = arcpy.da.ListDomains(model_catalog_path_sde)
        dict_of_scenarios = None
        for domain in list_of_domains:
            if domain.name == domain_name:
                dict_of_scenarios = domain.codedValues
                break
        return dict_of_scenarios

    @staticmethod
    def retrieve_engine_type_domain_as_dict(model_catalog_path_sde):
        return ModelCatalogDataIO.retrieve_domain_as_dict("Engine_Type",model_catalog_path_sde )

    #TODO - make this one 1-M
    @staticmethod
    def retrieve_model_alterations_domain_as_dict(model_catalog_path_sde):
        return ModelCatalogDataIO.retrieve_domain_as_dict("Model_Alterations", model_catalog_path_sde )

    @staticmethod
    def retrieve_model_purpose_domain_as_dict(model_catalog_path_sde):
        return ModelCatalogDataIO.retrieve_domain_as_dict("Model_Purpose", model_catalog_path_sde )

    @staticmethod
    def retrieve_model_status_domain_as_dict(model_catalog_path_sde):
        return ModelCatalogDataIO.retrieve_domain_as_dict("Model_Status", model_catalog_path_sde )

    @staticmethod
    def retrieve_proj_phase_domain_as_dict(model_catalog_path_sde):
        return ModelCatalogDataIO.retrieve_domain_as_dict("Proj_Phase", model_catalog_path_sde )

    @staticmethod
    def retrieve_proj_type_domain_as_dict(model_catalog_path_sde):
        return ModelCatalogDataIO.retrieve_domain_as_dict("Proj_Type", model_catalog_path_sde )