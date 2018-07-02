import arcpy
from modelCatalog_exception import ModelCatalog_exception, Field_names_length_does_not_match_row_length_exception

class DataIO():
    def __init__(self):
        pass

    def add_model(self, model, location, field_names):
        if not model.valid:
            raise ModelCatalog_exception

        row = [model.Parent_Model_ID, model.Model_Request_ID]

        if len(field_names) != len(row):
            raise Field_names_length_does_not_match_row_length_exception

        cursor = arcpy.da.InsertCursor(location, field_names)

        cursor.insertRow(row)
        del cursor


