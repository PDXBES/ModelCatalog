import mock
from unittest import TestCase
from businessclasses.model_catalog import ModelCatalog
from businessclasses.model import Model
from businessclasses.simulation import Simulation
from businessclasses.model_catalog_exception import InvalidModelException, DuplicateModelException, DuplicatesInInputModeList
from mock_config import MockConfig
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo

class TestModelCatalog(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.model_catalog = ModelCatalog(self.config)
        self.model1 = mock.MagicMock(Model)
        self.model1.id = 1
        self.model1.model_purpose_id = self.config.model_purpose_id["Calibration"]
        self.model1.simulations = []
        self.model2 = mock.MagicMock(Model)
        self.model2.id = 2
        self.model2.model_purpose_id = self.config.model_purpose_id["Characterization"]
        self.model2.simulations = []
        self.simulation1 = mock.MagicMock(Simulation)
        self.simulation1.id = 1
        self.simulation1.parent_id = 1
        self.simulation2 = mock.MagicMock(Simulation)
        self.simulation2.id = 2
        self.simulation2.parent_id = 2
        self.model_catalog_db_data_io = mock.MagicMock(ModelCatalogDbDataIo)
        self.model_catalog_db_data_io.workspace = "in_memory"

        self.patch_create_objects_from_database = mock.patch.object(self.model_catalog_db_data_io, "create_objects_from_database")
        self.mock_create_objects_from_database = self.patch_create_objects_from_database.start()

    def tearDown(self):
        self.mock_create_objects_from_database = self.patch_create_objects_from_database.stop()

    def test_model_check_for_duplicates(self):
        self.model1.valid = True
        self.model_catalog.models.append(self.model1)
        with self.assertRaises(DuplicateModelException):
            self.model_catalog.check_for_duplicate_model(self.model1)

    def test_model_check_for_valid(self):
        self.model1.valid = False
        self.model_catalog.models.append(self.model1)
        with self.assertRaises (InvalidModelException):
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

        with self.assertRaises(InvalidModelException):
            self.model_catalog.add_model(self.model1)

    def test_add_model_duplicate_model_should_fail(self):
        self.model1.valid = True
        self.model_catalog.add_model(self.model1)
        with self.assertRaises(DuplicateModelException):
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

        with self.assertRaises(InvalidModelException):
            self.model_catalog.add_models(models)

        self.assertEquals(len(self.model_catalog.models), 0)

    def test_add_model_list_add_duplicate_model_and_check_no_models_added(self):
        models = []

        self.model_catalog.models.append(self.model1)

        models.append(self.model1)

        with self.assertRaises(DuplicateModelException):
            self.model_catalog.add_models(models)

        self.assertEquals(len(self.model_catalog.models), 1)

    def test_add_model_list_add_duplicate_model_to_empty_list_and_check_no_models_added(self):
        models = []

        self.model_catalog.models = []

        self.model1.valid = True

        models.append(self.model1)
        models.append(self.model1)

        with self.assertRaises(DuplicatesInInputModeList):
            self.model_catalog.add_models(models)

        self.assertEquals(len(self.model_catalog.models), 0)

    def test_create_models_with_tracking_data_only_from_model_catalog_calls_copy_to_memory_with_correct_arguments(self):
        input_table = "model_tracking_sde_path"
        class_type = "model"
        self.model_catalog.create_models_with_tracking_data_only_from_model_catalog_db(self.model_catalog_db_data_io)
        self.mock_create_objects_from_database.assert_called_with(class_type, input_table)

    def test_create_models_with_tracking_data_only_from_model_catalog_returns_correct_value(self):
        self.mock_create_objects_from_database.return_value = "models"
        models = self.model_catalog.create_models_with_tracking_data_only_from_model_catalog_db(self.model_catalog_db_data_io)
        self.assertEqual(models, "models")

    def test_create_simulations_from_model_catalog_calls_copy_to_memory_with_correct_arguments(self):
        input_table = "simulation_sde_path"
        class_type = "simulation"
        self.model_catalog.create_simulations_from_model_catalog_db(self.model_catalog_db_data_io)
        self.mock_create_objects_from_database.assert_called_with(class_type, input_table)

    def test_create_simulations_from_model_catalog_returns_correct_value(self):
        self.mock_create_objects_from_database.return_value = "simulations"
        models = self.model_catalog.create_simulations_from_model_catalog_db(self.model_catalog_db_data_io)
        self.assertEqual(models, "simulations")

    def test_create_models_from_model_catalog_returns_correct_values(self):
        with mock.patch.object(self.model_catalog, "create_models_with_tracking_data_only_from_model_catalog_db") as mock_create_models_with_tracking_data_only:
            with mock.patch.object(self.model_catalog, "create_simulations_from_model_catalog_db") as mock_create_simulations:
                mock_create_models_with_tracking_data_only.return_value = [self.model1, self.model2]
                mock_create_simulations.return_value = [self.simulation1, self.simulation2]
                models = self.model_catalog.create_models_from_model_catalog_db(self.model_catalog_db_data_io)
                self.assertEqual(models[0], self.model1)
                self.assertEqual(models[0].simulations, [self.simulation1])
                self.assertEqual(models[1], self.model2)
                self.assertEqual(models[1].simulations, [self.simulation2])

                # make sure you add an empty list to mock models in setup for simulations, model alterations etc.

    def test_calibration_models_returns_list_of_calibration_models(self):
        self.model_catalog.models = [self.model1, self.model2]
        calibration_models = self.model_catalog.calibration_models()
        self.assertEqual(calibration_models, [self.model1])

