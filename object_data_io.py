import os
import arcpy
from config import Config
try:
    from typing import List, Any
except:
    pass
from generic_object import GenericObject


class ObjectDataIo():
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config

    def add_object(self, parent_id, object_class, field_attribute_lookup, object_tracking_sde_path):
        field_names = field_attribute_lookup.keys()

        cursor = arcpy.da.InsertCursor(object_tracking_sde_path, field_names)