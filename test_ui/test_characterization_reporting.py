import mock
from unittest import TestCase
from testbusinessclasses.mock_config import MockConfig
from businessclasses.model import Model
from businessclasses.model_catalog import ModelCatalog
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from ui.characterization_reporting import CharacterizationReporting

class TestCharacterizationReporting(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.model_catalog = mock.MagicMock(ModelCatalog)
        self.model_catalog_db_data_io = mock.MagicMock(ModelCatalogDbDataIo)

        self.characterization_reporting = CharacterizationReporting(self.config, self.model_catalog, self.model_catalog_db_data_io)

        self.model1 = mock.MagicMock(Model)
        self.model1.id = 1
        self.model1.model_purpose_id = self.config.model_purpose_id["Calibration"]
        self.model1.simulations = []
        self.model1.model_alterations = []
        self.model1.project_types = []
        self.model1.model_path = "model_path1"
        self.model1.create_date = "create_date1"
        self.model1.created_by = "created_by2"
        self.model2 = mock.MagicMock(Model)
        self.model2.id = 2
        self.model2.model_purpose_id = self.config.model_purpose_id["Characterization"]
        self.model2.simulations = []
        self.model2.model_alterations = []
        self.model2.project_types = []
        self.model2.model_path = "model_path2"
        self.model2.create_date = "create_date2"
        self.model2.created_by = "created_by2"
        self.model_string1 = self.model1.model_path + "   " + "date string" + "   " + self.model1.created_by
        self.model_string2 = self.model2.model_path + "   " + "date string" + "   " + self.model2.created_by

        self.characterization_reporting.characterization_model = {self.model_string1: self.model1,
                                                                  self.model_string2: self.model2}

        self.characterization_reporting.characterization_model_description = {self.model1: self.model_string1,
                                                                              self.model2: self.model_string2}



    def test_create_characterization_dictionary_calls_characterization_models(self):
        with mock.patch.object(self.model_catalog, "characterization_models") as mock_characterization_models:
            self.model_catalog.create_characterization_dictionary()
            self.assertTrue(mock_characterization_models.called)

    def test_create_characterization_dictionary_returns_formatted_list_of_strings(self):
        model_string1 = self.model1.model_path + "   " + "date string" + "   " + self.model1.created_by
        model_string2 = self.model2.model_path + "   " + "date string" + "   " + self.model2.created_by
        sample_characterization_models = {model_string1: self.model1, model_string2: self.model2}
        self.model1.model_purpose_id = self.config.model_purpose_id["Characterization"]
        with mock.patch.object(self.model_catalog, "characterization_models") as mock_characterization_models:
            with mock.patch.object(self.model_catalog, "format_date") as mock_format_date:
                mock_format_date.return_value = "date string"
                mock_characterization_models.return_value = [self.model1, self.model2]
                formatted_characterization_models = self.model_catalog.create_characterization_dictionary()

                self.assertEqual(sample_characterization_models.keys(), formatted_characterization_models.keys())

    def test_create_characterization_dictionary_returns_dictionary_with_models(self):
        model_string1 = self.model1.model_path + "   " + "date string" + "   " + self.model1.created_by
        model_string2 = self.model2.model_path + "   " + "date string" + "   " + self.model2.created_by
        sample_characterization_dictionary = {model_string1: self.model1, model_string2: self.model2}
        self.model1.model_purpose_id = self.config.model_purpose_id["Characterization"]
        with mock.patch.object(self.model_catalog, "characterization_models") as mock_characterization_models:
            with mock.patch.object(self.model_catalog, "format_date") as mock_format_date:
                mock_format_date.return_value = "date string"
                mock_characterization_models.return_value = [self.model1, self.model2]
                characterization_dictionary = self.model_catalog.create_characterization_dictionary()
                self.assertEqual(characterization_dictionary, sample_characterization_dictionary)


    def test_get_models_selected_from_characterization_reporting_selected_strings_returns_correct_models(self):
        model_strings = [self.model_string1, self.model_string2]
        models = [self.model1, self.model2]
        correct_models = self.characterization_reporting.get_models_selected_from_characterization_reporting(model_strings)
        self.assertEquals(correct_models, models)
