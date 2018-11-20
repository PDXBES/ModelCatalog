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
        self.name = "model_alt_hydrologic"

    def valid(self):
        return True