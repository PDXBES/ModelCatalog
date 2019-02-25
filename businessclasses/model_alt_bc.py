from config import Config
from model_alteration import ModelAlteration
try:
    from typing import List, Any
except:
    pass
from collections import OrderedDict

class ModelAltBc(ModelAlteration):

    def __init__(self, config):
        self.config = config
        super(ModelAltBc, self).__init__(self.config)
       #ModelAlteration.__init__(self, config)
        self.name = "model_alt_bc"

        self.input_field_attribute_lookup = OrderedDict()
        self.input_field_attribute_lookup["Model_ID"] = "parent_id"
        self.input_field_attribute_lookup["Model_Alt_BC_ID"] = "id"
        self.input_field_attribute_lookup["Model_Alteration_Domain_ID"] = "model_alteration_type_id"

    def valid(self):
        return True