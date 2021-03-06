import mock
from unittest import TestCase
from businessclasses.model_catalog import ModelCatalog
from businessclasses.model import Model
from businessclasses.simulation import Simulation
from businessclasses.model_alt_bc import ModelAltBc
from businessclasses.model_alt_hydraulic import ModelAltHydraulic
from businessclasses.model_alt_hydrologic import ModelAltHydrologic
from businessclasses.project_type import ProjectType
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
        self.simulation1 = mock.MagicMock(Simulation)
        self.simulation1.id = 1
        self.simulation1.parent_id = 1
        self.simulation2 = mock.MagicMock(Simulation)
        self.simulation2.id = 2
        self.simulation2.parent_id = 2

        self.model_alt_bc1 = mock.MagicMock(ModelAltBc)
        self.model_alt_bc1.id = 1
        self.model_alt_bc1.parent_id = 1
        self.model_alt_bc2 = mock.MagicMock(ModelAltBc)
        self.model_alt_bc2.id = 2
        self.model_alt_bc2.parent_id = 2

        self.model_alt_hydra1 = mock.MagicMock(ModelAltHydraulic)
        self.model_alt_hydra1.id = 1
        self.model_alt_hydra1.parent_id = 1
        self.model_alt_hydra2 = mock.MagicMock(ModelAltHydraulic)
        self.model_alt_hydra2.id = 2
        self.model_alt_hydra2.parent_id = 2

        self.model_alt_hydro1 = mock.MagicMock(ModelAltHydrologic)
        self.model_alt_hydro1.id = 1
        self.model_alt_hydro1.parent_id = 1
        self.model_alt_hydro2 = mock.MagicMock(ModelAltHydrologic)
        self.model_alt_hydro2.id = 2
        self.model_alt_hydro2.parent_id = 2

        self.proj_type1 = mock.MagicMock(ProjectType)
        self.proj_type1.id = 1
        self.proj_type1.parent_id = 1
        self.proj_type2 = mock.MagicMock(ProjectType)
        self.proj_type2.id = 2
        self.proj_type2.parent_id = 2

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

    def test_create_model_alt_bcs_from_model_catalog_calls_copy_to_memory_with_correct_arguments(self):
        input_table = "model_alt_bc_sde_path"
        class_type = "model_alt_bc"
        self.model_catalog.create_model_alt_bcs_from_model_catalog_db(self.model_catalog_db_data_io)
        self.mock_create_objects_from_database.assert_called_with(class_type, input_table)

    def test_create_model_alt_bcs_from_model_catalog_returns_correct_value(self):
        self.mock_create_objects_from_database.return_value = "model_alt_bcs"
        models = self.model_catalog.create_model_alt_bcs_from_model_catalog_db(self.model_catalog_db_data_io)
        self.assertEqual(models, "model_alt_bcs")

    def test_create_model_alt_hydraulics_from_model_catalog_calls_copy_to_memory_with_correct_arguments(self):
        input_table = "model_alt_hydraulic_sde_path"
        class_type = "model_alt_hydraulic"
        self.model_catalog.create_model_alt_hydraulics_from_model_catalog_db(self.model_catalog_db_data_io)
        self.mock_create_objects_from_database.assert_called_with(class_type, input_table)

    def test_create_model_alt_hydraulics_from_model_catalog_returns_correct_value(self):
        self.mock_create_objects_from_database.return_value = "model_alt_hydraulics"
        models = self.model_catalog.create_model_alt_hydraulics_from_model_catalog_db(self.model_catalog_db_data_io)
        self.assertEqual(models, "model_alt_hydraulics")

    def test_create_model_alt_hydrologics_from_model_catalog_calls_copy_to_memory_with_correct_arguments(self):
        input_table = "model_alt_hydrologic_sde_path"
        class_type = "model_alt_hydrologic"
        self.model_catalog.create_model_alt_hydrologics_from_model_catalog_db(self.model_catalog_db_data_io)
        self.mock_create_objects_from_database.assert_called_with(class_type, input_table)

    def test_create_model_alt_hydrologics_from_model_catalog_returns_correct_value(self):
        self.mock_create_objects_from_database.return_value = "model_alt_hydrologics"
        models = self.model_catalog.create_model_alt_hydrologics_from_model_catalog_db(self.model_catalog_db_data_io)
        self.assertEqual(models, "model_alt_hydrologics")

    def test_create_project_types_from_model_catalog_calls_copy_to_memory_with_correct_arguments(self):
        input_table = "project_type_sde_path"
        class_type = "project_type"
        self.model_catalog.create_project_types_from_model_catalog_db(self.model_catalog_db_data_io)
        self.mock_create_objects_from_database.assert_called_with(class_type, input_table)

    def test_create_project_types_from_model_catalog_returns_correct_value(self):
        self.mock_create_objects_from_database.return_value = "project_types"
        models = self.model_catalog.create_project_types_from_model_catalog_db(self.model_catalog_db_data_io)
        self.assertEqual(models, "project_types")

    def test_create_models_from_model_catalog_returns_correct_values(self):
        with mock.patch.object(self.model_catalog, "create_models_with_tracking_data_only_from_model_catalog_db") as mock_create_models_with_tracking_data_only:
            with mock.patch.object(self.model_catalog, "create_simulations_from_model_catalog_db") as mock_create_simulations:
                with mock.patch.object(self.model_catalog,
                                       "create_model_alt_bcs_from_model_catalog_db") as mock_create_model_alt_bcs:
                    with mock.patch.object(self.model_catalog,
                                           "create_model_alt_hydraulics_from_model_catalog_db") as mock_create_model_alt_hydraulics:
                        with mock.patch.object(self.model_catalog,
                                               "create_model_alt_hydrologics_from_model_catalog_db") as mock_create_model_alt_hydrologics:
                            with mock.patch.object(self.model_catalog,
                                                   "create_project_types_from_model_catalog_db") as mock_create_project_types:
                                mock_create_models_with_tracking_data_only.return_value = [self.model1, self.model2]
                                mock_create_simulations.return_value = [self.simulation1, self.simulation2]
                                mock_create_model_alt_bcs.return_value = [self.model_alt_bc1, self.model_alt_bc2]
                                mock_create_model_alt_hydraulics.return_value = [self.model_alt_hydra1, self.model_alt_hydra2]
                                mock_create_model_alt_hydrologics.return_value = [self.model_alt_hydro1, self.model_alt_hydro2]
                                mock_create_project_types.return_value = [self.proj_type1, self.proj_type2]
                                models = self.model_catalog.create_models_from_model_catalog_db(self.model_catalog_db_data_io)
                                self.assertEqual(models[0], self.model1)
                                self.assertEqual(models[0].simulations, [self.simulation1])
                                self.assertEqual(models[0].model_alterations, [self.model_alt_bc1, self.model_alt_hydra1, self.model_alt_hydro1])
                                self.assertEqual(models[0].project_types, [self.proj_type1])

                                self.assertEqual(models[1], self.model2)
                                self.assertEqual(models[1].simulations, [self.simulation2])
                                self.assertEqual(models[1].model_alterations, [self.model_alt_bc2, self.model_alt_hydra2, self.model_alt_hydro2])
                                self.assertEqual(models[1].project_types, [self.proj_type2])

    def test_calibration_models_returns_list_of_calibration_models(self):
        self.model_catalog.models = [self.model1, self.model2]
        calibration_models = self.model_catalog.calibration_models()
        self.assertEqual(calibration_models, [self.model1])

    def test_characterization_models_returns_list_of_characterization_models(self):
        self.model_catalog.models = [self.model1, self.model2]
        characterization_models = self.model_catalog.characterization_models()
        self.assertEqual(characterization_models, [self.model2])






