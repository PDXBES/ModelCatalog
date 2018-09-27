import arcpy
try:
    from typing import List, Any
except:
    pass

class DataIO:
    def __init__(self):
        self.current_id_database_table_path = None


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