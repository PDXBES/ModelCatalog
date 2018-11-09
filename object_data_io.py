import os
import arcpy
from config import Config
try:
    from typing import List, Any, Dict
except:
    pass
from generic_object import GenericObject
from db_data_io import DbDataIo

class ObjectDataIo():
    def __init__(self, config, db_data_io):
        # type: (Config, DbDataIo) -> None
        self.config = config
        self.db_data_io = db_data_io

    def add_object(self, parent_id, object_class, field_attribute_lookup, object_table_sde_path):
        # type: (int, GenericObject, Dict, str) -> None
        object_class.parent_id = parent_id
        object_class.id = self.db_data_io.retrieve_current_id(object_class.name)
        self.db_data_io.add_object(object_class, field_attribute_lookup, object_table_sde_path)


