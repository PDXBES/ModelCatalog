from businessclasses.config import Config
from dataio.utility import Utility

config = Config("TEST")
utility = Utility(config)

utility.model_catalog_test_data_cleanup()
utility.set_current_ids_to_zero(config.model_catalog_current_id_table_sde_path)
utility.rrad_test_data_cleanup()
utility.set_current_ids_to_zero(config.rrad_current_id_table_sde_path)
utility.rrad_mapping_test_data_cleanup()
utility.set_current_ids_to_zero(config.mapping_current_id_sde_path)

