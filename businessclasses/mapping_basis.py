from config import Config
from dataio.db_data_io import DbDataIo
from businessclasses.generic_class_factory import GenericClassFactory
from businessclasses.config import Config


class MappingBasis(DbDataIo):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.mapping_snapshots = []

        self.config = config
        self.current_id_database_table_path = self.config.model_catalog_current_id_table_sde_path
        self.workspace = "in_memory"
        self.class_factory = GenericClassFactory(self.config)
        self.class_factory.class_dict = {}

    #TODO add snapshot.  create in memory object
    #TODO Get current ids for each object type