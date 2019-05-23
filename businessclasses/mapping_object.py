from config import Config
from generic_object import GenericObject
from collections import OrderedDict


class MappingObject(GenericObject):

    def __init__(self, config):
        self.config = config
        self.snapshot_id = None
        self.simulation_id = None
        self.sim_desc = None
        self.geometry = None
        self.id = None

    @staticmethod
    def mapping_object_field_attribute_lookup():
        mapping_object_field_attribute_lookup = OrderedDict()
        mapping_object_field_attribute_lookup["Snapshot_ID"] = "snapshot_id"
        mapping_object_field_attribute_lookup["Simulation_ID"] = "simulation_id"
        return  mapping_object_field_attribute_lookup