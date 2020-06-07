
from dataio.utility import Utility


class ModelCopy(object):

    def __init__(self, config1, model_catalog, model_catalog_db_data_io):
        self.config = config1
        self.model_catalog = model_catalog
        self.model_catalog_db_data_io = model_catalog_db_data_io

        self.registered_models = None

    def create_registered_model_dictionary(self):
        model_dictionary = {}
        self.model_catalog.add_models_from_model_catalog_db(self.model_catalog_db_data_io)
        for model in self.model_catalog.models:
            model_string = model.model_path + "   " + Utility.format_date \
                (model.create_date) + "   " + model.created_by + " " + str(model.id)
            model_dictionary[model_string] = model
        self.registered_models = model_dictionary
