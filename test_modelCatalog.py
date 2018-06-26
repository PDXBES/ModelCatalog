from unittest import TestCase
from ModelCatalog import ModelCatalog
from Model import Model
import mock


class TestModelCatalog(TestCase):
    def setUp(self):
        self.model_catalog = ModelCatalog()
        #  self.model = Model()
        self.model1 = mock.MagicMock(Model)
        self.model2 = mock.MagicMock(Model)

    def test_add_model_new_model_into_empty_list(self):
        self.assertTrue(len(self.model_catalog.models) == 0)

        self.model_catalog.add_model(self.model1)

        self.assertEquals(self.model_catalog.models[-1], self.model1)
        self.assertTrue(len(self.model_catalog.models) == 1)

    def test_remove_model_first_in_list(self):

        self.model_catalog.models.append(self.model1)

        self.model_catalog.remove_model()

        self.assertFalse(self.model1 in self.model_catalog.models)

    def test_add_model_invalid_model_causes_exception(self):

        self.model1.valid = False

        with self.assertRaises(Exception):
            self.model_catalog.add_model(self.model1)


    def test_add_model_list_add_2_models_verify_2_models_in_catalog_models(self):
        models =[]

        self.model1.valid = True
        self.model2.valid = True

        models.append(self.model1)
        models.append(self.model2)

        self.model_catalog.add_models(models)

        self.assertTrue(self.model1 in self.model_catalog.models)



    def test_add_model_duplicate_model_should_fail(self):

        self.model_catalog.add_model(self.model1)
        with self.assertRaises(Exception):
            self.model_catalog.add_model(self.model1)





