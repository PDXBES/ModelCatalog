try:
    from typing import List, Any
except:
    pass
import traceback
from businessclasses.config import Config
from db_data_io import DbDataIo
from businessclasses.rehab import Rehab
from businessclasses.rehab_result import RehabResult
from businessclasses.area import Area
from collections import OrderedDict
from businessclasses.generic_class_factory import GenericClassFactory

class RradDbDataIo(DbDataIo):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.current_id_database_table_path = self.config.rrad_current_id_table_sde_path
        self.workspace = "in_memory"
        self.class_factory = GenericClassFactory(self.config)
        self.class_factory.class_dict = {"rehab_result": RehabResult, "rehab": Rehab, "area": Area}

    def retrieve_current_rehab_id(self):
        rehab_id = self.retrieve_current_id("rehab")
        return rehab_id

    #TODO: determine if this should be called append or stay as add for naming consistency
    def add_rehab(self, rehab, rehab_data_io):
        # type: (Rehab) -> None
        rehab.create_rehab_results(rehab_data_io)

        editor = rehab_data_io.start_editing_session(self.config.RRAD_sde_path)

        try:
            self.append_object_to_db(rehab,
                                     Rehab.input_field_attribute_lookup(),
                                     self.config.rehab_tracking_sde_path,
                                     self.config.rehab_tracking_sde_path)
            rehab_data_io.append_rehab_results(rehab)
            rehab_data_io.stop_editing_session(editor, True)
        except:
            rehab_data_io.stop_editing_session(editor, False)
            traceback.print_exc()



        



