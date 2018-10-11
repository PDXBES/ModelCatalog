import arcpy
from config import Config
try:
    from typing import List, Any
except:
    pass

from data_io_exception import DataIO_exception
from data_io_exception import Field_names_length_does_not_match_row_length_exception

class DataIO:
    def __init__(self, config):
        # type: (Config) -> None
        self.current_id_database_table_path = None
        self.config = config

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

    def add_object(self, object_class, field_attribute_lookup, object_tracking_sde_path):

        if not object_class.valid:
            raise DataIO_exception

        row = self.create_row_from_object(object_class, field_attribute_lookup )
        field_names = field_attribute_lookup.keys()

        if len(field_names) != len(row):
            raise Field_names_length_does_not_match_row_length_exception

        cursor = arcpy.da.InsertCursor(object_tracking_sde_path, field_names)

        cursor.insertRow(row)
        del cursor

    def create_row_from_object(self, generic_object, field_attribute_lookup):
        attribute_names = field_attribute_lookup.values()
        row = []
        try:
            for attribute_name in attribute_names:
                attribute_value = getattr(generic_object, attribute_name)
                row.append(attribute_value)
        except AttributeError:
            arcpy.AddMessage("When creating a row from a " + generic_object.name +
                  " the attribute " + attribute_name + " could not be found.")
            raise AttributeError
            #TODO find cleaner way to get traceback and stop program

        return row

#TODO - create separate dataIO for database and other