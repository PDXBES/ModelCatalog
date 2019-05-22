import arcpy
from businessclasses.config import Config
try:
    from typing import List, Any
except:
    pass
from data_io_exception import DataIoException
from data_io_exception import FieldNamesLengthDoesNotMatchRowLengthException

class DbDataIo(object):
    def __init__(self, config, class_factory):
        # type: (Config) -> None
        self.current_id_database_table_path = None
        self.config = config
        self.workspace = "in_memory"
        self.class_factory = class_factory

    def retrieve_current_id(self, object_type):
        # type: (str, str) -> int
        current_id = self.retrieve_block_of_ids(object_type, 1)
        return current_id

    def retrieve_block_of_ids(self, object_type, number_of_ids):
        if number_of_ids > 0:
            field_names = ["Object_Type", "Current_ID"]
            cursor = arcpy.da.UpdateCursor(self.current_id_database_table_path, field_names)
            for row in cursor:
                object_name, current_id = row
                if object_type == object_name:
                    next_id = current_id + number_of_ids
                    break
            cursor.updateRow([object_name, next_id])
            del cursor
        else:
            raise Exception()
        return current_id

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

    def create_object_from_row(self, generic_object, field_attribute_lookup, row):
        field_name_list = field_attribute_lookup.keys()
        for field_name, attribute_name in field_attribute_lookup.items():
            field_name_index = field_name_list.index(field_name)
            setattr(generic_object, attribute_name, row[field_name_index])

    def create_objects_from_table(self, table, class_type, field_attribute_lookup):
        generic_objects = []
        fields = field_attribute_lookup.keys()
        cursor = arcpy.da.SearchCursor(table, fields)
        for row in cursor:
            generic_object = self.class_factory.create_object(class_type)
            self.create_object_from_row(generic_object, field_attribute_lookup, row)
            generic_objects.append(generic_object)
        return generic_objects

    def create_objects_from_table_with_current_id(self, table, class_type, field_attribute_lookup):
        generic_objects = []
        fields = field_attribute_lookup.keys()
        number_of_objects = int(arcpy.GetCount_management(table)[0])
        current_id = self.retrieve_block_of_ids(class_type, number_of_objects)
        next_id = current_id + number_of_objects
        cursor = arcpy.da.SearchCursor(table, fields)
        for row in cursor:
            if current_id == next_id:
                raise Exception
            generic_object = self.class_factory.create_object(class_type)
            self.create_object_from_row(generic_object, field_attribute_lookup, row)
            generic_object.id = current_id
            current_id += 1
            generic_objects.append(generic_object)
        return generic_objects

    def create_objects_from_database(self, class_type, input_table_name):
        in_memory_output_table_name = "object_table"
        table = self.workspace + "/" + in_memory_output_table_name
        field_attribute_lookup = self.class_factory.class_dict[class_type].input_field_attribute_lookup()
        self.copy_to_memory(input_table_name, in_memory_output_table_name)
        objects = self.create_objects_from_table(table, class_type, field_attribute_lookup)
        arcpy.Delete_management(table)
        return objects

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

    def copy(self, input_table, target, field_mappings, parent_id_to_db_field_mapping, unique_id_field):
        # type: (str, str, arcpy.FieldMappings) -> None
        in_memory_table = self.workspace + "\\" + "copy_table"
        self.copy_to_memory(input_table, "copy_table")
        self.add_parent_id(in_memory_table, parent_id_to_db_field_mapping)
        self.add_unique_ids(in_memory_table, unique_id_field)
        if field_mappings != None:
            arcpy.Append_management(in_memory_table, target, "NO_TEST", field_mappings)
        else:
            field_mappings = self._create_field_map_for_sde_db(in_memory_table)

        arcpy.Append_management(in_memory_table, target, "NO_TEST", field_mappings)
        arcpy.Delete_management(in_memory_table)

    def copy_to_memory(self, input_table, in_memory_output_table_name):
        in_memory_table = self.workspace + "\\" + in_memory_output_table_name
        # TODO check if feature class or table and add logic
        try:
            arcpy.CopyFeatures_management(input_table, in_memory_table)
        except:
            arcpy.CopyRows_management(input_table, in_memory_table)

    def add_parent_id(self, in_memory_table, parent_id_to_db_field_mapping):
        for parent_id, db_id_field in parent_id_to_db_field_mapping:
            arcpy.AddField_management(in_memory_table, db_id_field, "LONG")
            arcpy.CalculateField_management(in_memory_table, db_id_field, parent_id, "PYTHON_9.3")

    def add_unique_ids(self, in_memory_table, unique_id_field):
        import uuid
        arcpy.AddField_management(in_memory_table, unique_id_field, "GUID")
        cursor = arcpy.da.UpdateCursor(in_memory_table, unique_id_field)
        for row in cursor:
            guid = '{' + str(uuid.uuid4()) + '}'
            row[0] = guid
            cursor.updateRow(row)
        del cursor

    def copy_db_to_db(self, input_table, target, field_mappings, parent_id_to_db_field_mapping):
        # type: (str, str, arcpy.FieldMappings) -> None
        if field_mappings != None:
            arcpy.Append_management(input_table, target, "NO_TEST", field_mappings)
        else:
            arcpy.Append_management(input_table, target, "NO_TEST")
        for parent_id, db_id_field in parent_id_to_db_field_mapping:
            arcpy.CalculateField_management(target, db_id_field, parent_id)

    def create_feature_class_from_objects(self, output_feature_class_name, object_list, field_attribute_lookup, template_feature_class_path):
        spatial_reference_template = template_feature_class_path
        try:
            arcpy.CreateFeatureclass_management(self.workspace, output_feature_class_name, "", template_feature_class_path, "", "", spatial_reference_template)
        except:
            arcpy.CreateTable_management(self.workspace, output_feature_class_name,template_feature_class_path)
        output_feature_class_path = self.workspace + "\\" + output_feature_class_name
        field_list = field_attribute_lookup.keys()
        cursor = arcpy.da.InsertCursor(output_feature_class_path, field_list)
        for generic_object in object_list:
            row = self.create_row_from_object(generic_object, field_attribute_lookup)
            cursor.insertRow(row)
        del cursor

    def append_object_to_db(self, object, field_attribute_lookup, template_table_path, target_path):
        self.append_objects_to_db([object], field_attribute_lookup, template_table_path, target_path)

    def append_objects_to_db(self, object_list, field_attribute_lookup, template_table_path, target_path):
        field_mappings = self._create_field_map_for_sde_db(template_table_path)
        output_feature_class_name = "intermediate_feature_class_to_append"
        self.create_feature_class_from_objects(output_feature_class_name, object_list, field_attribute_lookup, template_table_path)
        input_table = self.workspace + "\\" + output_feature_class_name
        arcpy.Append_management(input_table, target_path, "NO_TEST", field_mappings)
        arcpy.Delete_management(input_table)

    def copy_to_memory_with_id_filter(self, input_table, in_memory_output_table_name, id_field_name, id_list):
        in_memory_table = self.workspace + "\\" + in_memory_output_table_name
        where_clause = id_field_name + " in ("
        for count, id in enumerate(id_list):
            where_clause += str(id)
            if len(id_list) > 1 and count + 1 < len(id_list):
                where_clause += ","
        where_clause += ")"
        arcpy.MakeQueryTable_management(input_table, in_memory_table, "", "", "", where_clause)

    def create_objects_from_database_with_id_filter(self, class_type, input_table_name, id_field_name, id_list):
        in_memory_output_table_name = "object_table"
        table = self.workspace + "/" + in_memory_output_table_name
        field_attribute_lookup = self.class_factory.class_dict[class_type].input_field_attribute_lookup()
        self.copy_to_memory_with_id_filter(input_table_name, in_memory_output_table_name, id_field_name, id_list)
        objects = self.create_objects_from_table(table, class_type, field_attribute_lookup)
        arcpy.Delete_management(table)
        return objects








