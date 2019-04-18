from config import Config
from generic_object import GenericObject

class MappingSnapshot(GenericObject):
    def __init__(self, config):
        self.config = config
        self.id = None
        self.type = None
        self.business_rule = None
        self.mapping_links = []
        self.mapping_nodes = []
        self.mapping_areas = []


    def create_mapping_links(self):
        pass

    def create_mapping_nodes(self):
        pass

    def create_mapping_areas(self):
        pass