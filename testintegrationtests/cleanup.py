from businessclasses.config import Config
from dataio.utility import Utility

config = Config("TEST")
utility = Utility(config)

#utility.model_catalog_test_data_cleanup()
#utility.rrad_test_data_cleanup()
utility.rrad_mapping_test_data_cleanup()