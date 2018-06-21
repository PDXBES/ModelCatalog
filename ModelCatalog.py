
class ModelCatalog:
    def __init__(self):
        self.models = []

    def add_model(self, model):
        self.models.append(model)

    def remove_model(self):
        self.models.remove(self.models[0])