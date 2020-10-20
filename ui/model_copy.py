import os
import shutil
from datetime import datetime
from dataio.utility import Utility


class ModelCopy(object):

    def __init__(self, config1, model_catalog, model_catalog_db_data_io):
        self.config = config1
        self.model_catalog = model_catalog
        self.model_catalog_db_data_io = model_catalog_db_data_io

        self.registered_model_dict = None
        self.non_calibration_model_dict = None

    def create_registered_model_dictionary(self):
        model_dictionary = {}
        self.model_catalog.add_models_from_model_catalog_db(self.model_catalog_db_data_io)
        for model in self.model_catalog.models:
            model_string = model.model_name + "   " + model.model_path + "   " + model.created_by + "   " + Utility.format_date(model.create_date)
            model_dictionary[model_string] = model
        self.registered_model_dict = model_dictionary

    def create_non_calibration_model_dictionary(self):
        non_calibration_dictionary = {}
        self.model_catalog.add_models_from_model_catalog_db(self.model_catalog_db_data_io)
        non_calibration_models = self.model_catalog.non_calibration_models()
        for model in non_calibration_models:
            non_calibration_string = model.model_name + "   " + model.model_path + "   " + model.created_by + "   " + Utility.format_date(model.create_date)
            non_calibration_dictionary[non_calibration_string] = model
        self.non_calibration_model_dict = non_calibration_dictionary

    def copy_model_folder(self, model):
        source_folder = model.model_path
        new_dir = self.new_copy_dir_name(model)
        shutil.copytree(source_folder, new_dir)

    def new_copy_dir_name(self, model):
        new_folder_name = os.path.basename(model.model_path) + "_copy_" + datetime.now().strftime('%Y%m%d')
        destination_dir = os.path.dirname(model.model_path)
        new_dir = os.path.join(destination_dir, new_folder_name)
        return new_dir

    def get_selected_non_calibration_models(self, non_calibration_model_descriptions):
        non_calibration_models = []
        for non_calibration_model_description in non_calibration_model_descriptions:
            non_calibration_models.append(self.non_calibration_model_dict[non_calibration_model_description])
        return non_calibration_models

    def get_simulations_from_selected_models(self, model_descriptions):
        models = self.get_selected_non_calibration_models(model_descriptions)
        simulations = []
        for model in models:
            simulations += model.simulations
        return simulations