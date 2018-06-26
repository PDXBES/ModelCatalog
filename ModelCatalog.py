
class ModelCatalog:
    def __init__(self):
        self.models = []

    def add_model(self, model):
        if model in self.models:
            raise Exception

        if not model.valid:
            raise Exception

        self.models.append(model)

    def remove_model(self):
        self.models.remove(self.models[0])

    def add_models(self, models):
        for model in models:
            self.add_model(model)