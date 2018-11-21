from config import Config
from model_alteration import ModelAlteration
try:
    from typing import List, Any
except:
    pass
from collections import OrderedDict

class ModelAltHydraulic(ModelAlteration):

    def __init__(self, config):
        self.config = config
        super(ModelAltHydraulic, self).__init__(self.config)
       #ModelAlteration.__init__(self, config)
        self.name = "model_alt_hydraulic"

        self.field_attribute_lookup = OrderedDict()
        self.field_attribute_lookup["Model_ID"] = "parent_id"
        self.field_attribute_lookup["Model_Alt_Hydra_ID"] = "id"
        self.field_attribute_lookup["Model_Alteration_Domain_ID"] = "model_alteration_type_id"

    def valid(self):
        return True