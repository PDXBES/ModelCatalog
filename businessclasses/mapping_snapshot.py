from config import Config
from generic_object import GenericObject

class MappingSnapshot(GenericObject):
    def __init__(self, config):
        self.config = config
        self.id = None
        self.type = None
        self.business_rule = None


