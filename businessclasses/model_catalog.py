try:
    from typing import List, Any
except:
    pass
from model import Model
from model_catalog_exception import InvalidModelException, DuplicateModelException, DuplicatesInInputModeList
from config import Config
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
import arcpy

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

# TODO: finish below functions
    def create_models_with_tracking_data_only_from_model_catalog(self, model_catalog_db_data_io):
        # type: (ModelCatalogDbDataIo) -> None
        input_table_name = self.config.model_tracking_sde_path #to make generic
        class_type = "model"
        models = self.create_objects_from_model_catalog(class_type, input_table_name, model_catalog_db_data_io)
        return models # test that a list of models is returned

#could move this to db_data_io, but will not take model_catalog_db_data_io as it has self already
    def create_objects_from_model_catalog(self, class_type, input_table_name, model_catalog_db_data_io):
        in_memory_output_table_name = "object_table"
        table = model_catalog_db_data_io.workspace + "/" + in_memory_output_table_name
        field_attribute_lookup = Model.input_field_attribute_lookup()
        model_catalog_db_data_io.copy_to_memory(input_table_name, in_memory_output_table_name)
        objects = model_catalog_db_data_io.create_objects_from_table(table, class_type, field_attribute_lookup)
        arcpy.Delete_management(table)  # test this
        return objects

    #create a model to use the below static method
    # read from the sde path from the model tracking table
    # may need the model to access static method field_to_attribute_lookup
    # copy to memory( model_catalog_db_data_io)
    # create objects from that table in memory (model_catalog_db_data_io)
    # will return a list of models with only tracking data (to use with business classes)

    #repeat above with other tables (model alterations (hydro, hydra, bc) project_type, simulation) 5 additional functions


    def create_models_from_model_catalog(self, model_catalog_db_data_io):
        pass
    # Call above functions
    # for each model in the list, populate with data from the other 5 lists
    # use add_models to add them
