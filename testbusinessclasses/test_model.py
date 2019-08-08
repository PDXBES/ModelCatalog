from unittest import TestCase
from businessclasses.model import Model
import mock
from mock_config import MockConfig
from businessclasses.simulation import Simulation
from businessclasses.model_catalog_exception import InvalidCalibrationStormSimulationDescription
from businessclasses.model_catalog_exception import InvalidModelPurpose
from businessclasses.model_catalog_exception import InvalidProjectPhase
from dataio.model_data_io import ModelDataIo
from businessclasses.model_catalog_exception import InvalidModelRegistrationFileException


class TestModel(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.mock_db_data_io = mock.Mock()
        self.mock_db_data_io.retrieve_current_id.return_value = 1

        self.mock_model_data_io = mock.MagicMock(ModelDataIo)

        self.model = Model.initialize_with_current_id(self.config, self.mock_db_data_io)
        self.model.model_path = r"c:\temp"
        self.model.model_status_id = 0
        self.model.parent_model_path = r"parent_model_path"

        self.mock_simulation1 = mock.MagicMock(Simulation)
        self.mock_simulation1.storm_id = 1
        self.mock_simulation1.sim_desc = ""
        self.mock_simulation1.dev_scenario_id = 0

        self.mock_simulation2 = mock.MagicMock(Simulation)
        self.mock_simulation2.storm_id = 2
        self.mock_simulation2.sim_desc = ""
        self.mock_simulation2.dev_scenario_id = 1

        self.mock_calibration_simulation1 = mock.MagicMock(Simulation)
        self.mock_calibration_simulation1.storm_id = 0
        self.mock_calibration_simulation1.sim_desc = "20181225"

        self.mock_calibration_simulation2 = mock.MagicMock(Simulation)
        self.mock_calibration_simulation2.storm_id = 0
        self.mock_calibration_simulation2.sim_desc = "20191225"

        self.patch_os_path_exists = mock.patch("os.path.exists")
        self.mock_os_path_exists = self.patch_os_path_exists.start()

        self.patch_os_path_isfile = mock.patch("os.path.isfile")
        self.mock_os_path_isfile = self.patch_os_path_isfile.start()

        self.patch_read_model_id_from_model_registration_file = mock.patch.object(self.mock_model_data_io, "read_model_id_from_model_registration_file")
        self.mock_read_model_id_from_model_registration_file = self.patch_read_model_id_from_model_registration_file.start()
        self.mock_read_model_id_from_model_registration_file.return_value = 2233

    def tearDown(self):
        self.mock_os_path_exists = self.patch_os_path_exists.stop()
        self.mock_os_path_isfile = self.patch_os_path_isfile.stop()
        self.mock_read_model_id_from_model_registration_file = self.patch_read_model_id_from_model_registration_file.stop()


    def test_validate_model_path_called_with_correct_arguments(self):
        self.model.validate_model_path()
        self.mock_os_path_exists.assert_called_with(self.model.model_path)

    def test_validate_model_path_check_for_valid_path_if_valid_return_true(self):
        self.model.validate_model_path()
        self.assertTrue(self.mock_os_path_exists.called)

    def test_validate_model_path_check_for_valid_path_if_invalid_return_false(self):
        self.mock_os_path_exists.return_value = False
        is_valid = self.model.validate_model_path()
        self.assertEqual(is_valid, False)

    def test_validate_config_file_check_config_file_exists(self):
        self.model.validate_config_file()
        self.assertTrue(self.mock_os_path_isfile.called)

    def test_validate_config_file_called_with_correct_arguments(self):
        self.model.validate_config_file()
        self.mock_os_path_isfile.assert_called_with(self.model.model_path + "\\" + "emgaats.config")

    def test_validate_config_file_if_config_file_exists_return_true(self):
        self.mock_os_path_isfile.return_value = True
        is_valid = self.model.validate_config_file()
        self.assertTrue(is_valid)

    def test_validate_config_file_if_config_file_does_not_exist_return_false(self):
        self.mock_os_path_isfile.return_value = False
        is_valid = self.model.validate_config_file()
        self.assertEqual(is_valid, False)

    # TODO check that config file has valid values for ExtractionDateTime, ExtractionOriginalPath, EmgaatsVersion
    def test_validate_gdb_check_gdb_exists(self):
        self.model.validate_gdb()
        self.assertTrue(self.mock_os_path_exists.called)

    def test_validate_gdb_called_with_correct_arguments(self):
        self.model.validate_gdb()
        self.mock_os_path_exists.assert_called_with(self.model.model_path + "\\" + "EmgaatsModel.gdb")
   
    def test_validate_gdb_gdb_exists_return_true(self):
        self.mock_os_path_exists.return_value = True
        is_valid = self.model.validate_gdb()
        self.assertTrue(is_valid)

    def test_validate_gdb_gdb_file_does_not_exist_return_false(self):
        self.mock_os_path_exists.return_value = False
        is_valid = self.model.validate_gdb()
        self.assertEqual(is_valid, False)

    def test_validate_sim_check_sim_folder_exists(self):
        self.model.validate_sim()
        self.assertTrue(self.mock_os_path_exists.called)
   
    def test_validate_sim_called_with_correct_arguments(self):
        self.model.validate_sim()
        self.mock_os_path_exists.assert_called_with(self.model.model_path + "\\" + "sim")

    def test_validate_sim_sim_folder_exists_return_true(self):
        self.mock_os_path_exists.return_value = True
        is_valid = self.model.validate_sim()
        self.assertTrue(is_valid)

    def test_validate_sim_sim_folder_does_not_exist_return_false(self):
        self.mock_os_path_exists.return_value = False
        is_valid = self.model.validate_sim()
        self.assertEqual(is_valid, False)

    #TODO Write tests to for method to check for simulations

    @mock.patch("businessclasses.model.Model.validate_model_path")
    @mock.patch("businessclasses.model.Model.validate_config_file")
    @mock.patch("businessclasses.model.Model.validate_gdb")
    @mock.patch("businessclasses.model.Model.validate_sim")
    def test_valid_emgaats_model_structure_if_model_path_config_gdb_and_sim_are_valid_return_true(self, mock_validate_sim, mock_validate_gdb,
                                                   mock_validate_config_file, mock_validate_model_path):
        mock_validate_sim.return_value = True
        mock_validate_gdb.return_value = True
        mock_validate_config_file.return_value = True
        mock_validate_model_path.return_value = True
        is_valid = self.model.valid_emgaats_model_structure()
        self.assertTrue(is_valid)

    @mock.patch("businessclasses.model.Model.validate_model_path")
    @mock.patch("businessclasses.model.Model.validate_config_file")
    @mock.patch("businessclasses.model.Model.validate_gdb")
    @mock.patch("businessclasses.model.Model.validate_sim")
    def test_valid_emgaats_model_structure_if_model_path_invalid_return_false(self, mock_validate_sim, mock_validate_gdb,
                                                   mock_validate_config_file, mock_validate_model_path):
        mock_validate_sim.return_value = True
        mock_validate_gdb.return_value = True
        mock_validate_config_file.return_value = True
        mock_validate_model_path.return_value = False
        is_valid = self.model.valid_emgaats_model_structure()
        self.assertFalse(is_valid)

    @mock.patch("businessclasses.model.Model.validate_model_path")
    @mock.patch("businessclasses.model.Model.validate_config_file")
    @mock.patch("businessclasses.model.Model.validate_gdb")
    @mock.patch("businessclasses.model.Model.validate_sim")
    def test_valid_emgaats_model_structure_if_model_config_invalid_return_false(self, mock_validate_sim, mock_validate_gdb,
                                                   mock_validate_config_file, mock_validate_model_path):
        mock_validate_sim.return_value = True
        mock_validate_gdb.return_value = True
        mock_validate_config_file.return_value = False
        mock_validate_model_path.return_value = True
        is_valid = self.model.valid_emgaats_model_structure()
        self.assertFalse(is_valid)

    @mock.patch("businessclasses.model.Model.validate_model_path")
    @mock.patch("businessclasses.model.Model.validate_config_file")
    @mock.patch("businessclasses.model.Model.validate_gdb")
    @mock.patch("businessclasses.model.Model.validate_sim")
    def test_valid_if_gdb_invalid_return_false(self, mock_validate_sim, mock_validate_gdb,
                                                   mock_validate_config_file, mock_validate_model_path):
        mock_validate_sim.return_value = True
        mock_validate_gdb.return_value = False
        mock_validate_config_file.return_value = True
        mock_validate_model_path.return_value = True
        is_valid = self.model.valid
        self.assertFalse(is_valid)

    @mock.patch("businessclasses.model.Model.validate_model_path")
    @mock.patch("businessclasses.model.Model.validate_config_file")
    @mock.patch("businessclasses.model.Model.validate_gdb")
    @mock.patch("businessclasses.model.Model.validate_sim")
    def test_valid_emgaats_model_structure_if_sim_invalid_return_false(self, mock_validate_sim, mock_validate_gdb,
                                                   mock_validate_config_file, mock_validate_model_path):
        mock_validate_sim.return_value = False
        mock_validate_gdb.return_value = True
        mock_validate_config_file.return_value = True
        mock_validate_model_path.return_value = True
        is_valid = self.model.valid_emgaats_model_structure()
        self.assertFalse(is_valid)

    @mock.patch("businessclasses.model.Model.validate_model_path")
    @mock.patch("businessclasses.model.Model.validate_config_file")
    @mock.patch("businessclasses.model.Model.validate_gdb")
    @mock.patch("businessclasses.model.Model.validate_sim")
    def test_valid_emgaats_model_structure_if_all_invalid_return_false(self, mock_validate_sim, mock_validate_gdb,
                                                   mock_validate_config_file, mock_validate_model_path):
        mock_validate_sim.return_value = False
        mock_validate_gdb.return_value = False
        mock_validate_config_file.return_value = False
        mock_validate_model_path.return_value = False
        is_valid = self.model.valid_emgaats_model_structure()
        self.assertFalse(is_valid)

    def test_simulation_folder_path(self):
        sim_folder_path = r"c:\temp\sim"
        return_sim_folder_path = self.model.simulation_folder_path()
        self.assertEquals(sim_folder_path, return_sim_folder_path)

    def test_create_model_alt_bc_model_alt_bc_created_with_correct_attributes(self):
        alteration_type = "zero_bc"
        model_alt_bc = self.model.create_model_alt_bc(alteration_type, self.mock_db_data_io)
        self.assertEquals(model_alt_bc.model_alteration_type_id, 0)

    def test_create_model_alt_bc_nonexistant_type_throws_exception(self):
        alteration_type = "type that does not exist"
        with self.assertRaises(KeyError):
            self.model.create_model_alt_bc(alteration_type, self.mock_db_data_io)

    def test_create_model_alt_hydrologic_model_alt_hydrologic_created_with_correct_attributes(self):
        alteration_type = "zero_hydrologic"
        model_alt_hydrologic = self.model.create_model_alt_hydrologic(alteration_type, self.mock_db_data_io)
        self.assertEquals(model_alt_hydrologic.model_alteration_type_id, 0)

    def test_create_model_alt_hydrologic_nonexistant_type_throws_exception(self):
        alteration_type = "type that does not exist"
        with self.assertRaises(KeyError):
            self.model.create_model_alt_hydrologic(alteration_type, self.mock_db_data_io)

    def test_create_model_alt_hydraulic_model_alt_hydraulic_created_with_correct_attributes(self):
        alteration_type = "zero_hydraulic"
        model_alt_hydraulic = self.model.create_model_alt_hydraulic(alteration_type, self.mock_db_data_io)
        self.assertEquals(model_alt_hydraulic.model_alteration_type_id, 0)

    def test_create_model_alt_hydraulic_nonexistant_type_throws_exception(self):
        alteration_type = "type that does not exist"
        with self.assertRaises(KeyError):
            self.model.create_model_alt_hydraulic(alteration_type, self.mock_db_data_io)

    def test_create_model_alterations_model_with_bc_category_alterations_list_has_correct_values(self):
        alteration_types = [["zero_bc"], ["one_bc"], ["two_bc"]]
        alteration_category = "bc"
        self.model.create_model_alterations(alteration_types, alteration_category, self.mock_db_data_io)
        self.assertEquals(self.model.model_alterations[0].model_alteration_type_id, 0)
        self.assertEquals(self.model.model_alterations[1].model_alteration_type_id, 1)
        self.assertEquals(self.model.model_alterations[2].model_alteration_type_id, 2)

    def test_create_model_alterations_model_with_hydrologic_category_alterations_list_has_correct_values(self):
        alteration_types = [["zero_hydrologic"], ["one_hydrologic"], ["two_hydrologic"]]
        alteration_category = "hydrologic"
        self.model.create_model_alterations(alteration_types, alteration_category, self.mock_db_data_io)
        self.assertEquals(self.model.model_alterations[0].model_alteration_type_id, 0)
        self.assertEquals(self.model.model_alterations[1].model_alteration_type_id, 1)
        self.assertEquals(self.model.model_alterations[2].model_alteration_type_id, 2)

    def test_create_model_alterations_model_with_hydraulic_category_alterations_list_has_correct_values(self):
        alteration_types = [["zero_hydraulic"], ["one_hydraulic"], ["two_hydraulic"]]
        alteration_category = "hydraulic"
        self.model.create_model_alterations(alteration_types, alteration_category, self.mock_db_data_io)
        self.assertEquals(self.model.model_alterations[0].model_alteration_type_id, 0)
        self.assertEquals(self.model.model_alterations[1].model_alteration_type_id, 1)
        self.assertEquals(self.model.model_alterations[2].model_alteration_type_id, 2)

    def test_create_model_alterations_called_with_bc_category_calls_create_model_alt_bc(self):
        with mock.patch.object(self.model, "create_model_alt_bc") as mock_create_model_alt_bc:
            alteration_types = [["zero"], ["one"], ["two"]]
            alteration_category = "bc"
            self.model.create_model_alterations(alteration_types, alteration_category, self.mock_db_data_io)
            self.assertTrue(mock_create_model_alt_bc.called)

    def test_create_model_alterations_called_with_hydrologic_category_calls_create_model_alt_hydrologic(self):
        with mock.patch.object(self.model, "create_model_alt_hydrologic") as mock_create_model_alt_hydrologic:
            alteration_types = [["zero"], ["one"], ["two"]]
            alteration_category = "hydrologic"
            self.model.create_model_alterations(alteration_types, alteration_category, self.mock_db_data_io)
            self.assertTrue(mock_create_model_alt_hydrologic.called)

    def test_create_model_alterations_called_with_hydraulic_category_calls_create_model_alt_hydraulic(self):
        with mock.patch.object(self.model, "create_model_alt_hydraulic") as mock_create_model_alt_hydraulic:
            alteration_types = [["zero"], ["one"], ["two"]]
            alteration_category = "hydraulic"
            self.model.create_model_alterations(alteration_types, alteration_category, self.mock_db_data_io)
            self.assertTrue(mock_create_model_alt_hydraulic.called)

    def test_create_model_alterations_bc_calls_create_model_alterations_with_correct_argument(self):
        with mock.patch.object(self.model, "create_model_alterations") as mock_create_model_alterations:
            alteration_types = [["zero"], ["one"], ["two"]]
            self.model.create_model_alterations_bc(alteration_types, self.mock_db_data_io)
            mock_create_model_alterations.assert_called_with(alteration_types, "bc", self.mock_db_data_io)

    def test_create_model_alterations_hydrologic_calls_create_model_alterations_with_correct_argument(self):
        with mock.patch.object(self.model, "create_model_alterations") as mock_create_model_alterations:
            alteration_types = [["zero"], ["one"], ["two"]]
            self.model.create_model_alterations_hydrologic(alteration_types, self.mock_db_data_io)
            mock_create_model_alterations.assert_called_with(alteration_types, "hydrologic", self.mock_db_data_io)

    def test_create_model_alterations_hydraulic_calls_create_model_alterations_with_correct_argument(self):
        with mock.patch.object(self.model, "create_model_alterations") as mock_create_model_alterations:
            alteration_types = [["zero"], ["one"], ["two"]]
            self.model.create_model_alterations_hydraulic(alteration_types, self.mock_db_data_io)
            mock_create_model_alterations.assert_called_with(alteration_types, "hydraulic", self.mock_db_data_io)

    # TODO: write tests to verify diagnostic tools report appropriate errors

    def test_valid_calibration_simulations_model_has_two_calibration_storms_returns_true(self):
        self.model.simulations = [self.mock_simulation1, self.mock_simulation2, self.mock_calibration_simulation1, self.mock_calibration_simulation2]
        is_valid = self.model.valid_calibration_simulations()
        self.assertTrue(is_valid)

    def test_valid_calibration_simulations_model_has_two_calibration_storms_with_invalid_desc_length_returns_false(self):
        self.mock_calibration_simulation1.sim_desc = "FAKE20190203"
        self.model.simulations = [self.mock_simulation1, self.mock_simulation2, self.mock_calibration_simulation1, self.mock_calibration_simulation2]
        is_valid = self.model.valid_calibration_simulations()
        self.assertFalse(is_valid)

    def test_valid_calibration_simulations_model_has_two_calibration_storms_with_invalid_desc_date_returns_false(self):
        self.mock_calibration_simulation1.sim_desc = "20190250"
        self.model.simulations = [self.mock_simulation1, self.mock_simulation2, self.mock_calibration_simulation1, self.mock_calibration_simulation2]
        with self.assertRaises(InvalidCalibrationStormSimulationDescription):
            self.model.valid_calibration_simulations()

    def test_valid_calibration_simulations_model_has_two_calibration_storms_with_invalid_desc_string_in_date_returns_false(self):
        self.mock_calibration_simulation1.sim_desc = "2019025T"
        self.model.simulations = [self.mock_simulation1, self.mock_simulation2, self.mock_calibration_simulation1, self.mock_calibration_simulation2]
        with self.assertRaises(InvalidCalibrationStormSimulationDescription):
            self.model.valid_calibration_simulations()

    def test_valid_calibration_simulations_model_has_no_calibration_storms_returns_false(self):
        self.model.simulations = [self.mock_simulation1, self.mock_simulation2]
        is_valid = self.model.valid_calibration_simulations()
        self.assertFalse(is_valid)

    def test_valid_required_simulations_model_has_all_required_storms_returns_true(self):
        self.model.project_phase_id = self.config.proj_phase_id["Planning"]
        self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
        self.model.simulations = [self.mock_simulation1, self.mock_simulation2]
        is_valid = self.model.valid_required_simulations()
        self.assertTrue(is_valid)

    def test_valid_required_simulations_model_does_not_have_all_required_storms_returns_false(self):
        self.model.project_phase_id = self.config.proj_phase_id["Planning"]
        self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
        self.model.simulations = [self.mock_simulation1]
        is_valid = self.model.valid_required_simulations()
        self.assertFalse(is_valid)

    def test_valid_required_simulations_model_does_not_have_any_required_storms_returns_false(self):
        self.model.project_phase_id = self.config.proj_phase_id["Planning"]
        self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
        self.model.simulations = []
        is_valid = self.model.valid_required_simulations()
        self.assertFalse(is_valid)

    def test_required_storm_and_dev_scenario_ids_project_phase_planning_model_purpose_characterization_returns_correct_storm_dev_scenario_ids(self):
        self.model.project_phase_id = self.config.proj_phase_id["Planning"]
        self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
        required_storm_and_dev_scenario_ids = self.model.required_storm_and_dev_scenario_ids()
        self.assertEquals(required_storm_and_dev_scenario_ids, self.config.ccsp_characterization_storm_and_dev_scenario_ids)

    def test_required_storm_and_dev_scenario_ids_project_phase_planning_model_purpose_alternative_returns_correct_storm_dev_scenario_ids(self):
        self.model.project_phase_id = self.config.proj_phase_id["Planning"]
        self.model.model_purpose_id = self.config.model_purpose_id["Alternative"]
        required_storm_and_dev_scenario_ids = self.model.required_storm_and_dev_scenario_ids()
        self.assertEquals(required_storm_and_dev_scenario_ids, self.config.ccsp_alternative_storm_and_dev_scenario_ids)

    def test_required_storm_and_dev_scenario_ids_project_phase_planning_model_purpose_recommended_plan_returns_correct_storm_dev_scenario_ids(self):
        self.model.project_phase_id = self.config.proj_phase_id["Planning"]
        self.model.model_purpose_id = self.config.model_purpose_id["Recommended Plan"]
        required_storm_and_dev_scenario_ids = self.model.required_storm_and_dev_scenario_ids()
        self.assertEquals(required_storm_and_dev_scenario_ids, self.config.ccsp_recommended_plan_storm_and_dev_scenario_ids)

    def test_required_storm_and_dev_scenario_ids_invalid_model_purpose_raises_exception(self):
        self.model.model_purpose_id = 27
        with self.assertRaises(InvalidModelPurpose):
            self.model.required_storm_and_dev_scenario_ids()

    def test_required_storm_and_dev_scenario_ids_invalid_project_phase_raises_exception(self):
        self.model.project_phase_id = 27
        with self.assertRaises(InvalidProjectPhase):
            self.model.required_storm_and_dev_scenario_ids()

    def test_valid_working_model_valid_emgaats_structure_returns_true(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            mock_valid_emgaats_model_structure.return_value = True
            self.model.model_status_id = self.config.model_status_id["Working"]
            is_valid = self.model.valid
            self.assertTrue(is_valid)

    def test_valid_final_calibration_model_invalid_calls_valid_calibration_model_diagnostic(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_model_diagnostic") as mock_valid_calibration_model_diagnostic:
                with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                    self.model.model_purpose_id = self.config.model_purpose_id["Calibration"]
                    mock_valid_emgaats_model_structure.return_value = True
                    mock_valid_calibration_simulations.return_value = False
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    is_valid = self.model.valid
                    self.assertTrue(mock_valid_calibration_model_diagnostic.called)

    def test_valid_working_model_invalid_emgaats_structure_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            mock_valid_emgaats_model_structure.return_value = False
            self.model.model_status_id = self.config.model_status_id["Working"]
            is_valid = self.model.valid
            self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_predesign_valid_emgaats_structure_returns_true(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            mock_valid_emgaats_model_structure.return_value = True
            self.model.model_status_id = self.config.model_status_id["Final"]
            self.model.project_phase_id = self.config.proj_phase_id["Pre Design"]
            is_valid = self.model.valid
            self.assertTrue(is_valid)

    def test_valid_final_model_project_phase_predesign_invalid_emgaats_structure_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            mock_valid_emgaats_model_structure.return_value = False
            self.model.model_status_id = self.config.model_status_id["Final"]
            self.model.project_phase_id = self.config.proj_phase_id["Pre Design"]
            is_valid = self.model.valid
            self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_design30_valid_emgaats_structure_returns_true(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            mock_valid_emgaats_model_structure.return_value = True
            self.model.model_status_id = self.config.model_status_id["Final"]
            self.model.project_phase_id = self.config.proj_phase_id["Design 30"]
            is_valid = self.model.valid
            self.assertTrue(is_valid)

    def test_valid_final_model_project_phase_design30_invalid_emgaats_structure_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            mock_valid_emgaats_model_structure.return_value = False
            self.model.model_status_id = self.config.model_status_id["Final"]
            self.model.project_phase_id = self.config.proj_phase_id["Design 30"]
            is_valid = self.model.valid
            self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_design60_valid_emgaats_structure_returns_true(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            mock_valid_emgaats_model_structure.return_value = True
            self.model.model_status_id = self.config.model_status_id["Final"]
            self.model.project_phase_id = self.config.proj_phase_id["Design 60"]
            is_valid = self.model.valid
            self.assertTrue(is_valid)

    def test_valid_final_model_project_phase_design60_invalid_emgaats_structure_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            mock_valid_emgaats_model_structure.return_value = False
            self.model.model_status_id = self.config.model_status_id["Final"]
            self.model.project_phase_id = self.config.proj_phase_id["Design 60"]
            is_valid = self.model.valid
            self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_design90_valid_emgaats_structure_returns_true(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            mock_valid_emgaats_model_structure.return_value = True
            self.model.model_status_id = self.config.model_status_id["Final"]
            self.model.project_phase_id = self.config.proj_phase_id["Design 90"]
            is_valid = self.model.valid
            self.assertTrue(is_valid)

    def test_valid_final_model_project_phase_design90_invalid_emgaats_structure_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            mock_valid_emgaats_model_structure.return_value = False
            self.model.model_status_id = self.config.model_status_id["Final"]
            self.model.project_phase_id = self.config.proj_phase_id["Design 90"]
            is_valid = self.model.valid
            self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_calibration_valid_emgaats_structure_valid_calibration_simulation_returns_true(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                mock_valid_emgaats_model_structure.return_value = True
                mock_valid_calibration_simulations.return_value = True
                self.model.model_status_id = self.config.model_status_id["Final"]
                self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                self.model.model_purpose_id= self.config.model_purpose_id["Calibration"]
                is_valid = self.model.valid
                self.assertTrue(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_calibration_valid_emgaats_structure_invalid_calibration_simulation_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                mock_valid_emgaats_model_structure.return_value = True
                mock_valid_calibration_simulations.return_value = False
                self.model.model_status_id = self.config.model_status_id["Final"]
                self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                self.model.model_purpose_id= self.config.model_purpose_id["Calibration"]
                is_valid = self.model.valid
                self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_calibration_invalid_emgaats_structure_valid_calibration_simulation_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                mock_valid_emgaats_model_structure.return_value = False
                mock_valid_calibration_simulations.return_value = True
                self.model.model_status_id = self.config.model_status_id["Final"]
                self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                self.model.model_purpose_id= self.config.model_purpose_id["Calibration"]
                is_valid = self.model.valid
                self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_calibration_invalid_emgaats_structure_invalid_calibration_simulation_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                mock_valid_emgaats_model_structure.return_value = False
                mock_valid_calibration_simulations.return_value = False
                self.model.model_status_id = self.config.model_status_id["Final"]
                self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                self.model.model_purpose_id= self.config.model_purpose_id["Calibration"]
                is_valid = self.model.valid
                self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_characterization_valid_emgaats_structure_valid_required_simulation_returns_true(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = True
                    mock_valid_required_simulations.return_value = True
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id= self.config.model_purpose_id["Characterization"]
                    is_valid = self.model.valid
                    self.assertTrue(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_characterization_valid_emgaats_structure_invalid_required_simulation_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = True
                    mock_valid_required_simulations.return_value = False
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id= self.config.model_purpose_id["Characterization"]
                    is_valid = self.model.valid
                    self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_characterization_invalid_emgaats_structure_invalid_required_simulation_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = False
                    mock_valid_required_simulations.return_value = False
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id= self.config.model_purpose_id["Characterization"]
                    is_valid = self.model.valid
                    self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_alternative_valid_emgaats_structure_valid_required_simulation_returns_true(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = True
                    mock_valid_required_simulations.return_value = True
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id= self.config.model_purpose_id["Alternative"]
                    is_valid = self.model.valid
                    self.assertTrue(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_alternative_valid_emgaats_structure_invalid_required_simulation_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = True
                    mock_valid_required_simulations.return_value = False
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id= self.config.model_purpose_id["Alternative"]
                    is_valid = self.model.valid
                    self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_alternative_invalid_emgaats_structure_invalid_required_simulation_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = False
                    mock_valid_required_simulations.return_value = False
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id= self.config.model_purpose_id["Alternative"]
                    is_valid = self.model.valid
                    self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_recommended_plan_valid_emgaats_structure_valid_required_simulation_returns_true(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = True
                    mock_valid_required_simulations.return_value = True
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id= self.config.model_purpose_id["Recommended Plan"]
                    is_valid = self.model.valid
                    self.assertTrue(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_recommended_plan_valid_emgaats_structure_invalid_required_simulation_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = True
                    mock_valid_required_simulations.return_value = False
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id= self.config.model_purpose_id["Recommended Plan"]
                    is_valid = self.model.valid
                    self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_recommended_plan_invalid_emgaats_structure_invalid_required_simulation_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = False
                    mock_valid_required_simulations.return_value = False
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id= self.config.model_purpose_id["Recommended Plan"]
                    is_valid = self.model.valid
                    self.assertFalse(is_valid)

    def test_write_to_rrad_model_valid_model_status_final_project_phase_planning_model_purpose_not_calibration_returns_true(
            self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = True
                    mock_valid_required_simulations.return_value = True
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
                    ready_to_write_to_rrad = self.model.write_to_rrad()
                    self.assertTrue(ready_to_write_to_rrad)

    def test_write_to_rrad_model_not_valid_model_status_final_project_phase_planning_model_purpose_not_calibration_returns_false(
            self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = False
                    mock_valid_required_simulations.return_value = True
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
                    ready_to_write_to_rrad = self.model.write_to_rrad()
                    self.assertFalse(ready_to_write_to_rrad)

    def test_write_to_rrad_model_valid_model_status_working_project_phase_planning_model_purpose_not_calibration_returns_false(
            self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = True
                    mock_valid_required_simulations.return_value = True
                    self.model.model_status_id = self.config.model_status_id["Working"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
                    ready_to_write_to_rrad = self.model.write_to_rrad()
                    self.assertFalse(ready_to_write_to_rrad)

    def test_write_to_rrad_model_valid_model_status_final_project_phase_not_planning_model_purpose_not_calibration_returns_false(
            self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = True
                    mock_valid_required_simulations.return_value = True
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Pre Design"]
                    self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
                    ready_to_write_to_rrad = self.model.write_to_rrad()
                    self.assertFalse(ready_to_write_to_rrad)

    def test_write_to_rrad_model_valid_model_status_final_project_phase_planning_model_purpose_calibration_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = True
                    mock_valid_required_simulations.return_value = True
                    self.model.model_status_id = self.config.model_status_id["Final"]
                    self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                    self.model.model_purpose_id = self.config.model_purpose_id["Calibration"]
                    ready_to_write_to_rrad = self.model.write_to_rrad()
                    self.assertFalse(ready_to_write_to_rrad)

    def test_write_to_rrad_model_not_valid_model_model_status_working_project_phase_not_planning_model_purpose_calibration_returns_false(self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    mock_valid_emgaats_model_structure.return_value = False
                    mock_valid_required_simulations.return_value = True
                    self.model.model_status_id = self.config.model_status_id["Working"]
                    self.model.project_phase_id = self.config.proj_phase_id["Pre Design"]
                    self.model.model_purpose_id = self.config.model_purpose_id["Calibration"]
                    ready_to_write_to_rrad = self.model.write_to_rrad()
                    self.assertFalse(ready_to_write_to_rrad)


    def test_valid_registration_file_file_exists_returns_true(self):
        self.mock_os_path_isfile.return_value = True
        is_valid = self.model.valid_parent_model_registration_file()
        self.assertTrue(is_valid)

    def test_valid_registration_file_file_does_not_exist_returns_false(self):
        self.mock_os_path_isfile.return_value = False
        is_valid = self.model.valid_parent_model_registration_file()
        self.assertFalse(is_valid)


    def test_valid_final_model_project_phase_planning_model_purpose_characterization_valid_emgaats_structure_valid_required_simulation_valid_registration_file_returns_true(
            self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    with mock.patch.object(self.model, "validate_registration") as mock_validate_registration:
                        mock_valid_emgaats_model_structure.return_value = True
                        mock_valid_required_simulations.return_value = True
                        mock_validate_registration.return_value = True
                        self.model.model_status_id = self.config.model_status_id["Final"]
                        self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                        self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
                        is_valid = self.model.valid
                        self.assertTrue(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_alternative_valid_emgaats_structure_valid_required_simulation_valid_registration_file_returns_true(
            self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    with mock.patch.object(self.model, "validate_registration") as mock_validate_registration:
                        mock_valid_emgaats_model_structure.return_value = True
                        mock_valid_required_simulations.return_value = True
                        mock_validate_registration.return_value = True
                        self.model.model_status_id = self.config.model_status_id["Final"]
                        self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                        self.model.model_purpose_id = self.config.model_purpose_id["Alternative"]
                        is_valid = self.model.valid
                        self.assertTrue(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_recommended_plan_valid_emgaats_structure_valid_required_simulation_valid_registration_file_returns_true(
            self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    with mock.patch.object(self.model, "validate_registration") as mock_validate_registration:
                        mock_valid_emgaats_model_structure.return_value = True
                        mock_valid_required_simulations.return_value = True
                        mock_validate_registration.return_value = True
                        self.model.model_status_id = self.config.model_status_id["Final"]
                        self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                        self.model.model_purpose_id = self.config.model_purpose_id["Recommended Plan"]
                        is_valid = self.model.valid
                        self.assertTrue(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_characterization_valid_emgaats_structure_valid_required_simulation_invalid_registration_file_returns_false(
            self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    with mock.patch.object(self.model, "validate_registration") as mock_validate_registration:
                        mock_valid_emgaats_model_structure.return_value = True
                        mock_valid_required_simulations.return_value = True
                        mock_validate_registration.return_value = False
                        self.model.model_status_id = self.config.model_status_id["Final"]
                        self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                        self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
                        is_valid = self.model.valid
                        self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_alternative_valid_emgaats_structure_valid_required_simulation_invalid_registration_file_returns_false(
            self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    with mock.patch.object(self.model, "validate_registration") as mock_validate_registration:
                        mock_valid_emgaats_model_structure.return_value = True
                        mock_valid_required_simulations.return_value = True
                        mock_validate_registration.return_value = False
                        self.model.model_status_id = self.config.model_status_id["Final"]
                        self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                        self.model.model_purpose_id = self.config.model_purpose_id["Alternative"]
                        is_valid = self.model.valid
                        self.assertFalse(is_valid)

    def test_valid_final_model_project_phase_planning_model_purpose_recommended_plan_valid_emgaats_structure_valid_required_simulation_invalid_registration_file_returns_false(
            self):
        with mock.patch.object(self.model, "valid_emgaats_model_structure") as mock_valid_emgaats_model_structure:
            with mock.patch.object(self.model, "valid_calibration_simulations") as mock_valid_calibration_simulations:
                with mock.patch.object(self.model, "valid_required_simulations") as mock_valid_required_simulations:
                    with mock.patch.object(self.model, "validate_registration") as mock_validate_registration:
                        mock_valid_emgaats_model_structure.return_value = True
                        mock_valid_required_simulations.return_value = True
                        mock_validate_registration.return_value = False
                        self.model.model_status_id = self.config.model_status_id["Final"]
                        self.model.project_phase_id = self.config.proj_phase_id["Planning"]
                        self.model.model_purpose_id = self.config.model_purpose_id["Recommended Plan"]
                        is_valid = self.model.valid
                        self.assertFalse(is_valid)


    def test_valid_parent_model_purpose_calls_read_model_id_from_model_registration_file_with_parent_model(self):
        self.model.valid_parent_model_purpose()
        self.assertTrue(self.mock_model_data_io.read_model_id_from_model_registration_file.called)

    def test_set_parent_model_id_calls_read_model_id_from_model_registration_file(self):
        self.model.set_parent_model_id(self.mock_model_data_io)
        self.assertTrue(self.mock_model_data_io.read_model_id_from_model_registration_file.called)

    def test_set_parent_model_id_sets_parent_model_id(self):
        self.model.parent_model_id = 1111
        self.model.set_parent_model_id(self.mock_model_data_io)
        self.assertEquals(self.model.parent_model_id, 2233)

    def test_set_parent_model_id_model_purpose_calibration_parent_model_id_set_to_None(self):
        self.model.model_purpose_id = self.config.model_purpose_id["Calibration"]
        self.model.parent_model_id = 2
        self.model.set_parent_model_id(self.mock_model_data_io)
        self.assertEqual(self.model.parent_model_id, None)

    def test_set_parent_model_id_invalid_parent_model_registration_file_throws_InvalidModelRegistrationFileException(self):
        with mock.patch.object(self.model, "valid_parent_model_registration_file") as mock_valid_parent_model_registration_file:
            mock_valid_parent_model_registration_file.return_value = False
            self.model.parent_model_registration_file_path = "dummy_path"

            with self.assertRaises(InvalidModelRegistrationFileException):
                self.model.set_parent_model_id(self.mock_model_data_io)

    def test_valid_parent_model_purpose_model_purpose_characterization_parent_model_calibration_returns_true(self):
        parent_model_purpose = "Calibration"
        self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
        is_valid = self.model.valid_parent_model_purpose(parent_model_purpose)
        self.assertTrue(is_valid)

    def test_valid_parent_model_purpose_model_purpose_characterization_parent_model_alternative_returns_false(self):
        parent_model_purpose = "Alternative"
        self.model.model_purpose_id = self.config.model_purpose_id["Characterization"]
        is_valid = self.model.valid_parent_model_purpose(parent_model_purpose)
        self.assertFalse(is_valid)

    def test_valid_parent_model_purpose_model_purpose_calibration_parent_model_calibration_returns_true(self):
        parent_model_purpose = "Calibration"
        self.model.model_purpose_id = self.config.model_purpose_id["Calibration"]
        is_valid = self.model.valid_parent_model_purpose(parent_model_purpose)
        self.assertTrue(is_valid)

    def test_valid_parent_model_purpose_model_purpose_calibration_no_parent_model_returns_true(self):
        parent_model_purpose = None
        self.model.model_purpose_id = self.config.model_purpose_id["Calibration"]
        is_valid = self.model.valid_parent_model_purpose(parent_model_purpose)
        self.assertTrue(is_valid)

    def test_valid_parent_model_purpose_model_purpose_calibration_parent_model_alternative_returns_false(self):
        parent_model_purpose = "Alternative"
        self.model.model_purpose_id = self.config.model_purpose_id["Calibration"]
        is_valid = self.model.valid_parent_model_purpose(parent_model_purpose)
        self.assertFalse(is_valid)

    def test_valid_parent_model_purpose_model_purpose_alternative_parent_model_characterization_returns_true(self):
        parent_model_purpose = "Characterization"
        self.model.model_purpose_id = self.config.model_purpose_id["Alternative"]
        is_valid = self.model.valid_parent_model_purpose(parent_model_purpose)
        self.assertTrue(is_valid)

    def test_valid_parent_model_purpose_model_purpose_alternative_parent_model_calibration_returns_false(self):
        parent_model_purpose = "Calibration"
        self.model.model_purpose_id = self.config.model_purpose_id["Alternative"]
        is_valid = self.model.valid_parent_model_purpose(parent_model_purpose)
        self.assertFalse(is_valid)

    def test_valid_parent_model_purpose_model_purpose_recommended_plan_parent_model_characterization_returns_true(self):
        parent_model_purpose = "Characterization"
        self.model.model_purpose_id = self.config.model_purpose_id["Recommended Plan"]
        is_valid = self.model.valid_parent_model_purpose(parent_model_purpose)
        self.assertTrue(is_valid)

    def test_valid_parent_model_purpose_model_purpose_recommended_plan_parent_model_calibration_returns_false(self):
        parent_model_purpose = "Calibration"
        self.model.model_purpose_id = self.config.model_purpose_id["Recommended Plan"]
        is_valid = self.model.valid_parent_model_purpose(parent_model_purpose)
        self.assertFalse(is_valid)