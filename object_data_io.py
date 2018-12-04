import os
import arcpy
from config import Config
try:
    from typing import List, Any, Dict
except:
    pass
#from generic_object import GenericObject
from db_data_io import DbDataIo


class ObjectDataIo(object):
    def __init__(self, config, db_data_io):
        # type: (Config, DbDataIo) -> None
        self.config = config
        self.db_data_io = db_data_io

    def add_object(self, parent_id, generic_object, field_attribute_lookup, object_table_sde_path):
        # type: (int, GenericObject, Dict, str) -> None
        generic_object.parent_id = parent_id
        # object_class.id = self.db_data_io.retrieve_current_id(object_class.name)
        self.db_data_io.add_object(generic_object, field_attribute_lookup, object_table_sde_path)

    def start_editing_session(self, workspace_path):
        editor = arcpy.da.Editor(workspace_path)
        editor.startEditing(False, True)
        editor.startOperation()
        return editor

    def stop_editing_session(self, workspace_editor, save_changes):
        workspace_editor.stopOperation()
        workspace_editor.stopEditing(save_changes)

    def create_object(self, row, generic_object, field_attribute_lookup):
        # map from row fields to objects
        # create an object
        pass

    def create_objects(self, input_table, field_attribute_lookup):
        # calls search cursor
        # loop through rows
        # call create object
        # return list of objects
        pass

    def create_table_from_objects(self):
        pass

    def append_table_to_db(self):
        pass


