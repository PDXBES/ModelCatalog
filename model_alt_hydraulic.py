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

    def valid(self):
        return True