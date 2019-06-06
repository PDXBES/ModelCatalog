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
import datetime
from db_data_io import DbDataIo
from businessclasses.rehab import Rehab
from businessclasses.rrad import Rrad


class RradMappingDbDataIo(DbDataIo):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.mapping_snapshots = []

        self.config = config
        self.current_id_database_table_path = self.config.mapping_current_id_sde_path
        self.workspace = "in_memory"
        self.class_factory = GenericClassFactory(self.config)
        self.class_factory.class_dict = {"mapping_snapshot": MappingSnapshot,
                                         "mapping_node": MappingNode,
                                         "mapping_link": MappingLink,
                                         "mapping_area": MappingArea}

    def add_mapping_snapshot(self, mapping_snapshot, mapping_snapshot_data_io, rrad_db_data_io, rehab_data_io, rrad):
        rehab = rrad.create_rehab_for_characterization(rrad_db_data_io)
        rrad_db_data_io.add_rehab(rehab, rehab_data_io)

        mapping_snapshot.rehab_id = rehab.id

        mapping_snapshot.create_mapping_links(mapping_snapshot_data_io)
        mapping_snapshot.create_mapping_nodes(mapping_snapshot_data_io)
        mapping_snapshot.create_mapping_areas(mapping_snapshot_data_io)

        editor = mapping_snapshot_data_io.start_editing_session(self.config.RRAD_MAPPING_sde_path)

        try:
            self.append_object_to_db(mapping_snapshot, MappingSnapshot.input_field_attribute_lookup(),
                                     self.config.mapping_snapshot_tracking_sde_path,
                                     self.config.mapping_snapshot_tracking_sde_path)
            mapping_snapshot_data_io.append_mapping_links(mapping_snapshot)
            mapping_snapshot_data_io.append_mapping_nodes(mapping_snapshot)
            mapping_snapshot_data_io.append_mapping_areas(mapping_snapshot)

            mapping_snapshot_data_io.stop_editing_session(editor, True)
        except:
            mapping_snapshot_data_io.stop_editing_session(editor, False)
            arcpy.AddMessage("DB Error while adding snapshot. Changes rolled back.")
            traceback.print_exc()
            raise
#TODO: add snapshot- add snapshot to db