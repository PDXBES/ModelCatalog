import arcpy
from businessclasses.model_catalog import ModelCatalog
from businessclasses.model import Model
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from dataio.simulation_data_io import SimulationDataIo
from dataio.model_data_io import ModelDataIo
import getpass
import datetime
from dataio import utility
from businessclasses import config
from businessclasses.model_catalog_exception import InvalidModelException
from dataio.utility import Utility


class CharacterizationReporting(object):

    def __init__(self, config1, model_catalog, model_catalog_db_data_io):
        self.config = config1
        self.model_catalog = model_catalog
        self.model_catalog_db_data_io = model_catalog_db_data_io

        self.characterization_model = None

    def create_characterization_model_dictionary(self):
        characterization_dictionary = {}
        self.model_catalog.add_models_from_model_catalog_db(self.model_catalog_db_data_io)
        # TODO - only show valid models
        characterization_models = self.model_catalog.characterization_models()
        for model in characterization_models:
            characterization_string = model.model_path + "   " + Utility.format_date(model.create_date) + "   " + model.created_by
            characterization_dictionary[characterization_string] = model
        self.characterization_model = characterization_dictionary

    def get_models_selected_from_characterization_reporting(self, characterization_model_descriptions):
        characterization_models = []
        for characterization_model_description in characterization_model_descriptions:
            characterization_models.append(self.characterization_model[characterization_model_description])
        return characterization_models

    def get_simulations_from_selected_models(self, model_descriptions):
        models = self.get_models_selected_from_characterization_reporting(model_descriptions)
        simulations = []
        for model in models:
            simulations += model.simulations
        return simulations


    #TODO - in pyt? - get current ID and create snapshot record, populate (see add object)
    #TODO - in config - create snapshot type domain to go back and forth (text:int)

