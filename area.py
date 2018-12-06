from generic_object import GenericObject
from collections import OrderedDict
from config import Config
try:
    from typing import List, Any
except:
    pass

class Area(GenericObject):


    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.object_data_io = None
        self.parent_id = None
        self.field_attribute_lookup = None
        self.id = None
        self.name = "area"
        self.area_name = None
        self.first_floor_elev_ft = None
        self.first_floor_elev_qc = None
        self.has_basement = None
        self.has_basement_qc = None
        self.minDHGL = None
        self.maxHGL = None
        self.san_crown_elev_ft = None
        self.area_type = None
        self.field_attribute_lookup = Area.field_attribute_lookup()

    @staticmethod
    def field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["id"] = ["test"]
        return field_attribute_lookup












