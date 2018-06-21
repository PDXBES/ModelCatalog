from unittest import TestCase
from ModelCatalog import ModelCatalog
from Model import Model


class TestModelCatalog(TestCase):
    def setUp(self):
        self.model_catalog = ModelCatalog()
        self.model = Model()

    def test_add_model_new_model_in_list(self):
        #  model = MagicMock(model, spec: Model)
        self.model_catalog.add_model(self.model)

        self.assertEquals(self.model_catalog.models[-1], self.model)

    def test_remove_model_first_in_list(self):

        self.model_catalog.models.append(self.model)

        self.model_catalog.remove_model()

        self.assertFalse(self.model in self.model_catalog.models)





