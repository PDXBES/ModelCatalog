import arcpy
import time
from config import Config
try:
    from typing import List, Any
except:
    pass

from data_io_exception import DataIO_exception
from data_io_exception import Field_names_length_does_not_match_row_length_exception

class DbDataIo:
    def __init__(self, config):
        # type: (Config) -> None
        self.current_id_database_table_path = None
        self.config = config
        self.workspace = "in_memory"

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

    def add_object(self, object_class, field_attribute_lookup, object_table_sde_path):

        if not object_class.valid:
            raise DataIO_exception

        row = self.create_row_from_object(object_class, field_attribute_lookup )
        field_names = field_attribute_lookup.keys()

        if len(field_names) != len(row):
            raise Field_names_length_does_not_match_row_length_exception

        cursor = arcpy.da.InsertCursor(object_table_sde_path, field_names)

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

    def _create_field_map_for_sde_db(self, model_link_results_path):
        field_mappings = arcpy.FieldMappings()
        fields = arcpy.ListFields(model_link_results_path)
        for field in fields:
            if field.name == "SHAPE_Area" or field.name == "SHAPE_Length" or field.name == "OBJECTID" or field.name == "SHAPE":
                pass
            else:
                field_map = arcpy.FieldMap()
                field_map.addInputField(model_link_results_path, field.name)
                field_name = field_map.outputField
                field_name.name = field.name[0:31]
                field_map.outputField = field_name
                field_mappings.addFieldMap(field_map)

        return field_mappings

    def copy(self, input_table, target, field_mappings, parent_id_to_db_field_mapping):
        # type: (str, str, arcpy.FieldMappings) -> None
        in_memory_table = self.workspace + "\input_table"
        arcpy.CopyFeatures_management(input_table, in_memory_table)
        for parent_id, db_id_field in parent_id_to_db_field_mapping:
            arcpy.AddField_management(in_memory_table, db_id_field, "LONG")
            arcpy.CalculateField_management(in_memory_table, db_id_field, parent_id)

        if field_mappings != None:
            arcpy.Append_management(in_memory_table, target, "NO_TEST", field_mappings)
        else:
            field_mappings = self._create_field_map_for_sde_db(in_memory_table)
            arcpy.Append_management(in_memory_table, target, "NO_TEST", field_mappings)
        arcpy.Delete_management(in_memory_table)

    def copy_db_to_db(self, input_table, target, field_mappings, parent_id_to_db_field_mapping):
        # type: (str, str, arcpy.FieldMappings) -> None
        arcpy.AddMessage("Starting append")
        start_time = time.time()
        if field_mappings != None:
            arcpy.Append_management(input_table, target, "NO_TEST", field_mappings)
        else:
            arcpy.Append_management(input_table, target, "NO_TEST")
        end_time = time.time()
        arcpy.AddMessage((end_time - start_time))
        start_time = time.time()
        for parent_id, db_id_field in parent_id_to_db_field_mapping:
            arcpy.CalculateField_management(target, db_id_field, parent_id)
        end_time = time.time()
        arcpy.AddMessage((end_time - start_time))




