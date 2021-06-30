from businessclasses.config import Config
from dataio.utility import Utility

config = Config("TEST")
utility = Utility(config)

print("Cleaning model catalog test data")
utility.model_catalog_test_data_cleanup()
utility.set_current_ids_to_zero(config.model_catalog_current_id_table_sde_path)

