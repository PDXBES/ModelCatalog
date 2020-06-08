import os
import shutil
from datetime import datetime
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
                (model.create_date) + "   " + model.created_by + "   Model ID: " + str(model.id)
            model_dictionary[model_string] = model
        self.registered_models = model_dictionary

    def get_models_selected_from_model_dictionary(self, selected_model_descriptions):
        selected_models = []
        for model_description in selected_model_descriptions:
            selected_models.append(self.registered_models[model_description])
        return selected_models

    def copy_model_folder(self, model):
        source_folder = model.model_path
        new_dir = self.new_copy_dir_name(model)
        shutil.copytree(source_folder, new_dir)

    def new_copy_dir_name(self, model):
        new_folder_name = os.path.basename(model.model_path) + "_copy_" + datetime.now().strftime('%Y%m%d')
        destination_dir = os.path.dirname(model.model_path)
        new_dir = os.path.join(destination_dir, new_folder_name)
        return new_dir
