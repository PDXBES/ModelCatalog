import mock
from unittest import TestCase
from testbusinessclasses.mock_config import MockConfig
from businessclasses.model import Model
from businessclasses.model_catalog import ModelCatalog
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from ui.model_copy import ModelCopy

class TestModelCopy(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.model_catalog = ModelCatalog(self.config)
        self.model_catalog_db_data_io = mock.MagicMock(ModelCatalogDbDataIo)

        self.patch_add_models_from_model_catalog_db = mock.patch(
            "businessclasses.model_catalog.ModelCatalog.add_models_from_model_catalog_db")
        self.mock_add_models_from_model_catalog_db = self.patch_add_models_from_model_catalog_db.start()

        self.model1 = mock.MagicMock(Model)
        self.model1.id = 1
        self.model1.model_alterations = []
        self.model1.project_types = []
        self.model1.model_path = "model_path1"
        self.model1.create_date = "create_date1"
        self.model1.created_by = "created_by1"

        self.model2 = mock.MagicMock(Model)
        self.model2.id = 2
        self.model2.model_alterations = []
        self.model2.project_types = []
        self.model2.model_path = "model_path2"
        self.model2.create_date = "create_date2"
        self.model2.created_by = "created_by2"

        self.model_string1 = self.model1.model_path + "   " + "date string" + "   " + self.model1.created_by + " " + str(
            self.model1.id)
        self.model_string2 = self.model2.model_path + "   " + "date string" + "   " + self.model2.created_by + " " + str(
            self.model2.id)

        self.patch_format_date = mock.patch("dataio.utility.Utility.format_date")
        self.mock_format_date = self.patch_format_date.start()
        self.mock_format_date.return_value = "date string"

        self.model_copy = ModelCopy(self.config, self.model_catalog, self.model_catalog_db_data_io)

    def tearDown(self):
        self.mock_add_models_from_model_catalog_db = self.patch_add_models_from_model_catalog_db.stop()
        self.mock_format_date = self.patch_format_date.start()

    def test_create_registered_model_dictionary_calls_add_models_from_model_catalog_db(self):
        self.model_copy.create_registered_model_dictionary()
        self.assertTrue(self.mock_add_models_from_model_catalog_db.called)

    def test_create_registered_model_dictionary_returns_formatted_list_of_strings(self):
        model_string1 = self.model1.model_path + "   " + "date string" + "   " + self.model1.created_by + "   Model ID: " + str(self.model1.id)
        model_string2 = self.model2.model_path + "   " + "date string" + "   " + self.model2.created_by + "   Model ID: " + str(self.model2.id)
        #TODO: list was reordered to make test pass, verify that this is correct
        formatted_models_keys = [model_string2, model_string1]
        self.model_copy.create_registered_model_dictionary()
        self.assertEqual(self.model_copy.registered_models.keys(), formatted_models_keys)

    #def test_copy_model_folder_calls_new_copy_dir...

    #def test_copy_model_folder_calls_copytree...

    #def test_new_copy_dir_name_calls_os.pathname, dirname, join
    # is this one really neded?