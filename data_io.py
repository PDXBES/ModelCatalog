import arcpy
try:
    from typing import List, Any
except:
    pass

from data_io_exception import DataIO_exception
from data_io_exception import Field_names_length_does_not_match_row_length_exception
class DataIO:
    def __init__(self):
        self.current_id_database_table_path = None
        self.field_names = []


    def retrieve_current_id(self, object_type):
        # type: (str, str) -> int
        field_names = ["Object_Type", "Current_ID"]
        cursor = arcpy.da.UpdateCursor(self.current_id_database_table_path, field_names)
        for row in cursor:
            object_name, current_id = row
            if object_type == object_name:
                next_id = current_id + 1
                break
        cursor.updateRow([object_name, next_id])
        return current_id

    def map_object_attributes_to_database_fields(self, object_class):
        pass

    def add_object(self, object_class):

        if not object_class.valid:
            raise DataIO_exception

        row = self.map_object_attributes_to_database_fields()

        if len(self.field_names) != len(row):
            raise Field_names_length_does_not_match_row_length_exception

        cursor = arcpy.da.InsertCursor(self.config.model_tracking_sde_path, self.field_names)

        cursor.insertRow(row)
        del cursor
