from generic_object import GenericObject
from config import Config
try:
    from typing import List, Any
except:
    pass
from collections import OrderedDict

class ProjectType(GenericObject):

    def __init__(self, config):
        # type: (Config) -> None
        self.id = None
        self.name = "project_type"
        self.project_type_id = None
        self.config = config

        self.input_field_attribute_lookup = ProjectType.input_field_attribute_lookup()

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Model_ID"] = "parent_id"
        field_attribute_lookup["Project_Type_ID"] = "id"
        field_attribute_lookup["Project_Type_Domain_ID"] = "project_type_id"
        return field_attribute_lookup

    def valid(self):
        return True
