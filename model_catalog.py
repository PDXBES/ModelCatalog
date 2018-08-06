from typing import List, Any
from model import Model
from model_catalog_exception import Invalid_Model_exception, Duplicate_model_Exception, Duplicates_in_input_model_list


class ModelCatalog:
    models = None  # type: List[Model]

    def __init__(self):
        self.models = []

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
                raise Duplicates_in_input_model_list

    def check_for_duplicate_model(self, model):
        # type: (model) -> None
        if model in self.models:
            raise Duplicate_model_Exception

    def check_for_valid_model(self, model):
        # type: (model) -> None
        if not model.valid:
            raise Invalid_Model_exception
