import arcpy
import os
from model_catalog_exception import ModelCatalog_exception, Field_names_length_does_not_match_row_length_exception
from typing import List, Any
from model import Model

class ModelCatalogDataIO():
    def __init__(self):
        connections = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\Model_Catalog\Dev\connection_files"
        MODELCATALOG_sde = r"BESDBTEST1.MODELCATALOG.sde"
        self.MODEL_CATALOG = os.path.join(connections, MODELCATALOG_sde)
        self.ValueTable = self.MODEL_CATALOG + r"\MODEL_CATALOG.GIS.VAT_MaxVal"
        self.ModelTracking = self.MODEL_CATALOG + r"\MODEL_CATALOG.GIS.ModelTracking"
        pass

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






#import os
# #from model import Model
# connections = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\Model_Catalog\Dev\connection_files"
# MODELCATALOG_sde = r"BESDBTEST1.MODELCATALOG.sde"
# MODEL_CATALOG = os.path.join(connections, MODELCATALOG_sde)
# ModelTracking = MODEL_CATALOG + r"\MODEL_CATALOG.GIS.ModelTracking"
# ValueTable = MODEL_CATALOG + r"\MODEL_CATALOG.GIS.VAT_MaxVal"
# ModelTracking = MODEL_CATALOG + r"\MODEL_CATALOG.GIS.ModelTracking"
# dataio = DataIO()
# model = Model()
# current_id = dataio.retrieve_next_model_id(ValueTable, ["Object_Type", "Current_ID"])
#
# field_names = [
#     "Model_ID",
#     "Parent_Model_ID",
#     "Model_Request_ID",
#     "Project_Phase",
#     "Engine_Type",
#     "Create_Date",
#     "Deploy_Date",
#     "Run_Date",
#     "Model_Path",
#     "Project_Type",
#     "Model_Purpose",
#     "Model_Calibration_file",
#     "Model_Status",
#     "Model_Alterations",
#     "Model_Alteration_file",
#     "Project_Num"]
#
# model.Model_ID = current_id
# model.valid = True
# dataio.add_model(model,  ModelTracking, field_names)
