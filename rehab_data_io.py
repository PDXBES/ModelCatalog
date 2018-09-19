import arcpy
try:
    from typing import List, Any
except:
    pass
from config import Config


class RehabDataIO():
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config

    def select_nbcr_data_pipes(self):
        arcpy.SelectLayerByAttribute_management(self.config.rehab_nbcr_data_sde_path, "NEW_SELECTION", "hservstat not in ( 'ABAN' , 'TBAB' , 'DNE' ) and cutno = 0 and compkey is not Null")
    #TODO may want to break up query into pieces