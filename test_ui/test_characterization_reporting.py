import mock
from unittest import TestCase
from testbusinessclasses.mock_config import MockConfig
from businessclasses.model import Model
from businessclasses.simulation import Simulation
from businessclasses.model_catalog import ModelCatalog
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from ui.characterization_reporting import CharacterizationReporting

class TestCharacterizationReporting(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.model_catalog = ModelCatalog(self.config)
        self.model_catalog_db_data_io = mock.MagicMock(ModelCatalogDbDataIo)

        self.patch_add_models_from_model_catalog_db = mock.patch("businessclasses.model_catalog.ModelCatalog.add_models_from_model_catalog_db")
        self.mock_add_models_from_model_catalog_db = self.patch_add_models_from_model_catalog_db.start()

        self.simulation1 = mock.MagicMock(Simulation)
        self.simulation2 = mock.MagicMock(Simulation)
        self.simulation3 = mock.MagicMock(Simulation)

        self.model1 = mock.MagicMock(Model)
        self.model1.id = 1
        self.model1.model_purpose_id = self.config.model_purpose_id["Characterization"]
        self.model1.simulations = [self.simulation1]
        self.model1.model_alterations = []
        self.model1.project_types = []
        self.model1.model_path = "model_path1"
        self.model1.create_date = "create_date1"
        self.model1.created_by = "created_by2"
        self.model2 = mock.MagicMock(Model)
        self.model2.id = 2
        self.model2.model_purpose_id = self.config.model_purpose_id["Characterization"]
        self.model2.simulations = [self.simulation2, self.simulation3]
        self.model2.model_alterations = []
        self.model2.project_types = []
        self.model2.model_path = "model_path2"
        self.model2.create_date = "create_date2"
        self.model2.created_by = "created_by2"
        self.model_string1 = self.model1.model_path + "   " + "date string" + "   " + self.model1.created_by
        self.model_string2 = self.model2.model_path + "   " + "date string" + "   " + self.model2.created_by

        self.patch_characterization_models = mock.patch("businessclasses.model_catalog.ModelCatalog.characterization_models")
        self.mock_characterization_models = self.patch_characterization_models.start()
        self.mock_characterization_models.return_value = [self.model1, self.model2]

        self.patch_format_date = mock.patch("dataio.utility.Utility.format_date")
        self.mock_format_date = self.patch_format_date.start()
        self.mock_format_date.return_value = "date string"

        self.characterization_reporting = CharacterizationReporting(self.config, self.model_catalog,
                                                                    self.model_catalog_db_data_io)

        self.test_characterization_model = {self.model_string1: self.model1,
                                                                  self.model_string2: self.model2}

    def tearDown(self):
        self.mock_add_models_from_model_catalog_db = self.patch_add_models_from_model_catalog_db.stop()
        self.mock_characterization_models = self.patch_characterization_models.stop()
        self.mock_format_date = self.patch_format_date.start()

    def test_create_characterization_model_dictionary_calls_add_models_from_model_catalog_db(self):
        self.characterization_reporting.create_characterization_model_dictionary()
        self.assertTrue(self.mock_add_models_from_model_catalog_db.called)

    def test_create_characterization_model_dictionary_calls_characterization_models(self):
        self.characterization_reporting.create_characterization_model_dictionary()
        self.assertTrue(self.mock_characterization_models.called)

    def test_create_characterization_model_dictionary_sets_characterization_model_to_correct_value(self):
        self.characterization_reporting.create_characterization_model_dictionary()
        self.assertEquals(self.test_characterization_model, self.characterization_reporting.characterization_model)

    def test_create_characterization_model_dictionary_returns_formatted_list_of_strings(self):
        model_string1 = self.model1.model_path + "   " + "date string" + "   " + self.model1.created_by
        model_string2 = self.model2.model_path + "   " + "date string" + "   " + self.model2.created_by
        formatted_characterization_models_keys = [model_string1, model_string2]
        self.characterization_reporting.create_characterization_model_dictionary()
        self.assertEqual(self.characterization_reporting.characterization_model.keys(), formatted_characterization_models_keys)

    def test_get_models_selected_from_characterization_reporting_selected_strings_returns_correct_models(self):
        model_descriptions = [self.model_string1, self.model_string2]
        models = [self.model1, self.model2]
        self.characterization_reporting.characterization_model = self.test_characterization_model
        correct_models = self.characterization_reporting.get_models_selected_from_characterization_reporting(model_descriptions)
        self.assertEquals(correct_models, models)

    def test_get_simulations_from_selected_models_calls_get_models_selected_from_characterization_reporting_called_with_correct_arguments(self):
        model_descriptions = [self.model_string1, self.model_string2]
        with mock.patch.object(self.characterization_reporting, "get_models_selected_from_characterization_reporting") as mock_get_models_selected_from_characterization_reporting:
            self.characterization_reporting.get_simulations_from_selected_models(model_descriptions)
            mock_get_models_selected_from_characterization_reporting.assert_called_with(model_descriptions)

    def test_get_simulations_from_selected_models_returns_correct_simulations(self):
        model_descriptions = [self.model_string1, self.model_string2]
        with mock.patch.object(self.characterization_reporting, "get_models_selected_from_characterization_reporting") as mock_get_models_selected_from_characterization_reporting:
            mock_get_models_selected_from_characterization_reporting.return_value = [self.model1, self.model2]
            simulations_list = self.characterization_reporting.get_simulations_from_selected_models(model_descriptions)
            correct_simulations = [self.simulation1, self.simulation2, self.simulation3]
            self.assertEqual(simulations_list, correct_simulations)