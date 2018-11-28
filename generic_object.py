from object_data_io import ObjectDataIo
from config import Config
try:
    from typing import List, Any, Dict
except:
    pass

class GenericObject(object):
    def __init__(self, config):
        self.config = config
        self.object_data_io = None
        self.id = None
        self.name = None
        self.parent_id = None
        self.field_attribute_lookup = None

    @classmethod
    def initialize_with_current_id(cls, config, object_data_io):
        # type: (Config, ObjectDataIo) -> GenericObject
        generic_object = cls(config)
        db_data_io = object_data_io.db_data_io
        generic_object_current_id = db_data_io.retrieve_current_id(generic_object.name)
        generic_object.id = generic_object_current_id
        generic_object.object_data_io = object_data_io
        return generic_object

    @property
    def valid(self):
        # type: () -> bool
        return False
