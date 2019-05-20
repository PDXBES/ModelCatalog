from businessclasses.generic_class_factory import GenericClassFactory
from businessclasses.config import Config
from businessclasses.mapping_snapshot import MappingSnapshot
from businessclasses.mapping_node import MappingNode
from businessclasses.mapping_link import MappingLink
from businessclasses.mapping_area import MappingArea
from dataio.rrad_db_data_io import RradDbDataIo
from dataio.rehab_data_io import RehabDataIo
import arcpy
import traceback
from db_data_io import DbDataIo
class RradMappingDbDataIo(DbDataIo):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.mapping_snapshots = []

        self.config = config
        self.current_id_database_table_path = self.config.mapping_current_id_sde_path
        self.workspace = "in_memory"
        #self.workspace = r"C:\Users\bfreeman\Desktop\snapshot.gdb"
        self.class_factory = GenericClassFactory(self.config)
        self.class_factory.class_dict = {"mapping_snapshot": MappingSnapshot,
                                         "mapping_node": MappingNode,
                                         "mapping_link": MappingLink,
                                         "mapping_area": MappingArea}

    def add_mapping_snapshot(self, mapping_snapshot, mapping_snapshot_data_io):
        # create rrad_db_data_io
        # create rehab_data_io
        #call create_rehab_results_snapshot from rehab_data_io
        # this will get us a rehab_id

        rrad_db_data_io = RradDbDataIo(self.config)
        rehab_data_io = RehabDataIo(self.config, rrad_db_data_io)
        mapping_snapshot.rehab_id = rehab_data_io.create_rehab_snapshot_for_characterization_mapping_snapshot()

        editor = mapping_snapshot_data_io.start_editing_session(self.config.RRAD_MAPPING_sde_path)

        try:
            self.append_object_to_db(mapping_snapshot, MappingSnapshot.input_field_attribute_lookup(),
                                     self.config.mapping_snapshot_tracking_sde_path,
                                     self.config.mapping_snapshot_tracking_sde_path)

            mapping_snapshot.create_mapping_links(mapping_snapshot_data_io)
            mapping_snapshot.create_mapping_nodes(mapping_snapshot_data_io)
            mapping_snapshot.create_mapping_areas(mapping_snapshot_data_io)

            mapping_snapshot_data_io.append_mapping_links(mapping_snapshot)
            mapping_snapshot_data_io.append_mapping_nodes(mapping_snapshot)
            mapping_snapshot_data_io.append_mapping_areas(mapping_snapshot)

            mapping_snapshot_data_io.stop_editing_session(editor, True)
        except:
            mapping_snapshot_data_io.stop_editing_session(editor, False)
            arcpy.AddMessage("DB Error while adding model. Changes rolled back.")
            traceback.print_exc()
            raise
#TODO: add snapshot- add snapshot to db