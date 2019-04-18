from config import Config
from generic_object import GenericObject
from collections import OrderedDict


class MappingObject(GenericObject):

    def __init__(self):
        self.snapshot_id = None
        self.simulation_id = None
        self.sim_desc = None
        self.geometry = None

    @staticmethod
    def mapping_object_field_attribute_lookup():
        mapping_object_field_attribute_lookup = OrderedDict()
        mapping_object_field_attribute_lookup["Shape@"] = "geometry"
        mapping_object_field_attribute_lookup["Snapshot_ID"] = "snapshot_id"
        mapping_object_field_attribute_lookup["Simulation_ID"] = "simulation_id"
        return  mapping_object_field_attribute_lookup