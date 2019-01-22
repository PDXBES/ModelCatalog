import arcpy
try:
    from typing import List, Any
except:
    pass
from config import Config
from db_data_io import DbDataIo
from rehab import Rehab
from pipe import Pipe
from collections import OrderedDict
from generic_class_factory import GenericClassFactory

class RradDbDataIo(DbDataIo):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.current_id_database_table_path = self.config.rrad_current_id_table_sde_path
        self.field_attribute_lookup = OrderedDict()
        self.field_attribute_lookup["Rehab_ID"] = "id"
        self.field_attribute_lookup["Extract_Date"] = "extract_date"
        self.field_attribute_lookup["Last_Inspection_Date"] = "last_inspection_date"
        self.field_attribute_lookup["Purpose"] = "purpose"
        self.class_factory = GenericClassFactory(self.config)
        self.class_factory.class_dict = {"pipe": Pipe(), "rehab": Rehab(self.config)}

    def retrieve_current_rehab_id(self):
        rehab_id = self.retrieve_current_id("rehab")
        return rehab_id

    def add_rehab(self, rehab):
        # type: (Rehab) -> None
        self.add_object(rehab, self.field_attribute_lookup, self.config.rehab_tracking_sde_path)
