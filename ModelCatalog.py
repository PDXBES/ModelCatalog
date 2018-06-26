#TODO throw more specific exceptions

class ModelCatalog:
    def __init__(self):
        self.models = []

    def add_model(self, model):
        self.check_for_duplicate_model(model)

        self.check_for_valid_model(model)

        self.models.append(model)

    def remove_model(self):
        self.models.remove(self.models[0])

    def add_models(self, models):
        for model in models:
            self.check_for_duplicate_model(model)
        for model in models:
            self.check_for_valid_model(model)

        model_set = set()
        for model in models:
            if model not in model_set:
                model_set.add(model)
            else:
                raise Exception

        for model in models:
            self.add_model(model)

    def check_for_duplicate_model(self, model):
        if model in self.models:
            raise Exception

    def check_for_valid_model(self, model):
        if not model.valid:
            raise Exception
