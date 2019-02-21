from generic_object import GenericObject
from config import Config
try:
    from typing import List, Any
except:
    pass
from collections import OrderedDict

class ModelAlteration(GenericObject):

    def __init__(self, config):
        # type: (Config) -> None
        self.id = None
        self.name = "model_alteration"
        self.model_alteration_type_id = None
        self.config = config

        # self.input_field_attribute_lookup = OrderedDict()
        # self.input_field_attribute_lookup["Model_ID"] = "parent_id"
        # self.input_field_attribute_lookup["Model_Alteration_ID"] = "id"
        # self.input_field_attribute_lookup["Model_Alteration_Domain_ID"] = "model_alteration_type_id"
