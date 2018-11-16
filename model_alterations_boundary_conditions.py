from config import Config
from model_alteration import ModelAlteration
try:
    from typing import List, Any
except:
    pass
from collections import OrderedDict

class ModelAlterationsBoundaryConditions(ModelAlteration):

    def __init__(self, config):

        super(ModelAlterationsBoundaryConditions, self).__init__(self.config)
       #ModelAlteration.__init__(self, config)
        self.name = "model_alterations_boundary_conditions"

