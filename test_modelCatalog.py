import mock
from unittest import TestCase
from ModelCatalog import ModelCatalog
from Model import Model
from modelCatalog_exception import  Invalid_Model_exception,  Duplicate_model_Exception, Duplicates_in_input_model_list


class TestModelCatalog(TestCase):
    def setUp(self):
        self.model_catalog = ModelCatalog()
        self.model1 = mock.MagicMock(Model)
        self.model2 = mock.MagicMock(Model)

    def test_model_check_for_duplicates(self):
        self.model1.valid = True
        self.model_catalog.models.append(self.model1)
        with self.assertRaises(Exception):
            self.model_catalog.check_for_duplicate_model(self.model1)

    def test_model_check_for_valid(self):
        self.model1.valid = False
        self.model_catalog.models.append(self.model1)
        with self.assertRaises (Exception):
            self.model_catalog.check_for_valid_model(self.model1)

    def test_add_model_new_model_into_empty_list(self):
        self.model1.valid = True
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

        with self.assertRaises(Invalid_Model_exception):
            self.model_catalog.add_model(self.model1)

    def test_add_model_duplicate_model_should_fail(self):
        self.model1.valid = True
        self.model_catalog.add_model(self.model1)
        with self.assertRaises(Duplicate_model_Exception):
            self.model_catalog.add_model(self.model1)

    def test_add_model_list_add_2_models_verify_2_models_in_catalog_models(self):
        models = []

        self.model1.valid = True
        self.model2.valid = True

        models.append(self.model1)
        models.append(self.model2)

        self.model_catalog.add_models(models)

        self.assertTrue(self.model1 in self.model_catalog.models)

    def test_add_model_list_1_model_valid_1_model_invalid(self):
        models = []

        self.model_catalog.models = []

        self.model1.valid = True
        self.model2.valid = False

        models.append(self.model1)
        models.append(self.model2)

        with self.assertRaises(Invalid_Model_exception):
            self.model_catalog.add_models(models)

        self.assertEquals(len(self.model_catalog.models), 0)

    def test_add_model_list_add_duplicate_model_and_check_no_models_added(self):
        models = []

        self.model_catalog.models.append(self.model1)

        models.append(self.model1)

        with self.assertRaises(Duplicate_model_Exception):
            self.model_catalog.add_models(models)

        self.assertEquals(len(self.model_catalog.models), 1)

    def test_add_model_list_add_duplicate_model_to_empty_list_and_check_no_models_added(self):
        models = []

        self.model_catalog.models = []

        self.model1.valid = True

        models.append(self.model1)
        models.append(self.model1)

        with self.assertRaises(Exception):
            self.model_catalog.add_models(models)

        self.assertEquals(len(self.model_catalog.models), 0)







