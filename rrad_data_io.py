import arcpy
try:
    from typing import List, Any
except:
    pass
from config import Config
from data_io import DataIO

class RradDataIO(DataIO):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.current_id_database_table_path = self.config.rrad_current_id_table_sde_path

    def retrieve_current_rehab_id(self):
        rehab_id = self.retrieve_current_id("rehab")
        return rehab_id