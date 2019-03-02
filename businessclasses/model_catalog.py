try:
    from typing import List, Any
except:
    pass
from model import Model
from model_catalog_exception import InvalidModelException, DuplicateModelException, DuplicatesInInputModeList
from config import Config
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo

class ModelCatalog:
    models = None  # type: List[Model]

    def __init__(self, config):
        # type: (Config) -> None
        self.models = []
        self.config = config

    def add_model(self, model):
        # type: (Model) -> None
        self.check_for_duplicate_model(model)
        self.check_for_valid_model(model)
        self.models.append(model)

    def remove_model(self):
        self.models.remove(self.models[0])

    def add_models(self, models):
        # type: (List[Model]) -> None
        for model in models:
            self.check_for_duplicate_model(model)
        for model in models:
            self.check_for_valid_model(model)

        self.check_for_duplicates_in_input_model_list(models)

        for model in models:
            self.add_model(model)

    def check_for_duplicates_in_input_model_list(self, models):
        # type: (List[Model]) -> None
        model_set = set()
        for model in models:
            if model not in model_set:
                model_set.add(model)
            else:
                raise DuplicatesInInputModeList

    def check_for_duplicate_model(self, model):
        # type: (Model) -> None
        if model in self.models:
            raise DuplicateModelException

    def check_for_valid_model(self, model):
        # type: (Model) -> None
        if not model.valid:
            raise InvalidModelException

    def create_models_with_tracking_data_only_from_model_catalog_db(self, model_catalog_db_data_io):
        # type: (ModelCatalogDbDataIo) -> None
        input_table_name = self.config.model_tracking_sde_path
        class_type = "model"
        models = model_catalog_db_data_io.create_objects_from_database(class_type, input_table_name)
        return models

    def create_simulations_from_model_catalog_db(self, model_catalog_db_data_io):
        # type: (ModelCatalogDbDataIo) -> None
        input_table_name = self.config.simulation_sde_path
        class_type = "simulation"
        simulations = model_catalog_db_data_io.create_objects_from_database(class_type, input_table_name)
        return simulations


    #create a model to use the below static method
    # read from the sde path from the model tracking table
    # may need the model to access static method field_to_attribute_lookup
    # copy to memory( model_catalog_db_data_io)
    # create objects from that table in memory (model_catalog_db_data_io)
    # will return a list of models with only tracking data (to use with business classes)

    #repeat above with other tables (model alterations (hydro, hydra, bc) project_type, simulation) 5 additional functions

    # Call above functions
    # for each model in the list, populate with data from the other 5 lists
    # use add_models to add them

    def create_models_from_model_catalog_db(self, model_catalog_db_data_io):
        models = self.create_models_with_tracking_data_only_from_model_catalog_db(model_catalog_db_data_io)
        simulations = self.create_simulations_from_model_catalog_db(model_catalog_db_data_io)
        for model in models:
            for simulation in simulations:
                if simulation.parent_id == model.id:
                    model.simulations.append(simulation)
        return models

    def add_models_from_model_catalog_db(self, model_catalog_db_data_io):
        self.add_models(self.create_models_from_model_catalog_db(model_catalog_db_data_io))

    def calibration_models(self):
        calibration_models = []
        for model in self.models:
            if self.config.model_purpose[model.model_purpose_id] == "Calibration":
                calibration_models.append(model)
        return calibration_models



