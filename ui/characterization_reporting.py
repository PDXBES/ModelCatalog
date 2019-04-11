import arcpy
from businessclasses.model_catalog import ModelCatalog
from businessclasses.model import Model
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from dataio.simulation_data_io import SimulationDataIO
from dataio.model_data_io import ModelDataIo
import getpass
import datetime
from dataio import utility
from businessclasses import config
from businessclasses.model_catalog_exception import InvalidModelException

class CharacterizationReporting(object):

    def __init__(self, config, model_catalog):
        self.config = config
        self.model_catalog = model_catalog