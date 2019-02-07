try:
    from typing import List, Any
except:
    pass
from model import Model
from model_catalog_exception import InvalidModelException, DuplicateModelException, DuplicatesInInputModeList
from config import Config
import arcpy

class ModelCatalog:
    models = None  # type: List[Model]

    def __init__(self, config):
        # type: (Config) -> None
        self.models = []
        self.config = config

    def add_model(self, model):
        # type: (model) -> None
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
        # type: (model) -> None
        if model in self.models:
            raise DuplicateModelException

    def check_for_valid_model(self, model):
        # type: (model) -> None
        if not model.valid:
            raise InvalidModelException
