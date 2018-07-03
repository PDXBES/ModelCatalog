import arcpy
from modelCatalog_exception import ModelCatalog_exception, Field_names_length_does_not_match_row_length_exception

class DataIO():
    def __init__(self):
        pass

    def retrieve_next_model_id(self, location, field_names):
        cursor = arcpy.da.UpdateCursor(location, field_names)
        object_name, current_id = cursor.next()
        next_id = current_id + 1
        cursor.updateRow([object_name, next_id])
        return current_id

    def add_model(self, model, location, field_names):
        if not model.valid:
            raise ModelCatalog_exception

        row = [model.Model_ID, model.Parent_Model_ID,
               model.Model_Request_ID, model.Project_Phase, model.Engine_Type, model.Create_Date,
               model.Deploy_Date, model.Run_Date, model.Model_Path, model.Project_Type,
               model.Model_Purpose, model.Model_Calibration_file, model.Model_Status,
               model.Model_Alterations, model.Model_Alteration_file, model.Project_Num]

        if len(field_names) != len(row):
            raise Field_names_length_does_not_match_row_length_exception

        cursor = arcpy.da.InsertCursor(location, field_names)

        cursor.insertRow(row)
        del cursor

import os
from Model import Model
connections = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\Model_Catalog\Dev\connection_files"
MODELCATALOG_sde = r"BESDBTEST1.MODELCATALOG.sde"
MODEL_CATALOG = os.path.join(connections, MODELCATALOG_sde)
ModelTracking = MODEL_CATALOG + r"\MODEL_CATALOG.GIS.ModelTracking"
ValueTable = MODEL_CATALOG + r"\MODEL_CATALOG.GIS.VAT_MaxVal"
ModelTracking = MODEL_CATALOG + r"\MODEL_CATALOG.GIS.ModelTracking"
dataio = DataIO()
model = Model()
current_id = dataio.retrieve_next_model_id(ValueTable, ["Object_Type", "Current_ID"])

field_names = [
    "Model_ID",
    "Parent_Model_ID",
    "Model_Request_ID",
    "Project_Phase",
    "Engine_Type",
    "Create_Date",
    "Deploy_Date",
    "Run_Date",
    "Model_Path",
    "Project_Type",
    "Model_Purpose",
    "Model_Calibration_file",
    "Model_Status",
    "Model_Alterations",
    "Model_Alteration_file",
    "Project_Num"]

model.Model_ID = current_id
model.valid = True
dataio.add_model(model,  ModelTracking, field_names)
