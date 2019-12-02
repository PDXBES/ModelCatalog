from config import Config
from model_alteration import ModelAlteration
try:
    from typing import List, Any
except:
    pass
from collections import OrderedDict

class ModelAltHydrologic(ModelAlteration):

    def __init__(self, config):
        self.config = config
        super(ModelAltHydrologic, self).__init__(self.config)
       #ModelAlteration.__init__(self, config)
        self.input_field_attribute_lookup = ModelAltHydrologic.input_field_attribute_lookup()

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Model_ID"] = "parent_id"
        field_attribute_lookup["Model_Alt_Hydro_ID"] = "id"
        field_attribute_lookup["Model_Alteration_Domain_ID"] = "model_alteration_type_id"
        return field_attribute_lookup

    def valid(self):
        return True