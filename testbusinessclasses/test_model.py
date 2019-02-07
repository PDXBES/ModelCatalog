from unittest import TestCase
from businessclasses.model import Model
import mock
from mock_config import MockConfig
from businessclasses.simulation import Simulation
from businessclasses.model_catalog_exception import InvalidCalibrationStormSimulationDescription

class TestModel(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.mock_object_data_io = mock.Mock()
        self.mock_object_data_io.db_data_io.retrieve_current_id.return_value = 1
        self.model = Model.initialize_with_current_id(self.config, self.mock_object_data_io)
        self.model.model_path = r"c:\temp"

        self.mock_simulation1 = mock.MagicMock(Simulation)
        self.mock_simulation1.storm_id = 1
        self.mock_simulation1.sim_desc = ""
        self.mock_simulation1.dev_scenario_id = 0

        self.mock_simulation2 = mock.MagicMock(Simulation)
        self.mock_simulation2.storm_id = 2
        self.mock_simulation2.sim_desc = ""
        self.mock_simulation1.dev_scenario_id = 1

        self.mock_calibration_simulation1 = mock.MagicMock(Simulation)
        self.mock_calibration_simulation1.storm_id = 0
        self.mock_calibration_simulation1.sim_desc = "TAG20181225"

        self.mock_calibration_simulation2 = mock.MagicMock(Simulation)
        self.mock_calibration_simulation2.storm_id = 0
        self.mock_calibration_simulation2.sim_desc = "TAG20191225"

        self.patch_os_path_exists = mock.patch("os.path.exists")
        self.mock_os_path_exists = self.patch_os_path_exists.start()

        self.patch_os_path_isfile = mock.patch("os.path.isfile")
        self.mock_os_path_isfile = self.patch_os_path_isfile.start()

    def tearDown(self):
        self.mock_os_path_exists = self.patch_os_path_exists.stop()
        self.mock_os_path_isfile = self.patch_os_path_isfile.stop()

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
        model_alt_bc = self.model.create_model_alt_bc(alteration_type)
        self.assertEquals(model_alt_bc.model_alteration_type_id, 0)

    def test_create_model_alt_bc_nonexistant_type_throws_exception(self):
        alteration_type = "type that does not exist"
        with self.assertRaises(KeyError):
            self.model.create_model_alt_bc(alteration_type)

    def test_create_model_alt_hydrologic_model_alt_hydrologic_created_with_correct_attributes(self):
        alteration_type = "zero_hydrologic"
        model_alt_hydrologic = self.model.create_model_alt_hydrologic(alteration_type)
        self.assertEquals(model_alt_hydrologic.model_alteration_type_id, 0)

    def test_create_model_alt_hydrologic_nonexistant_type_throws_exception(self):
        alteration_type = "type that does not exist"
        with self.assertRaises(KeyError):
            self.model.create_model_alt_hydrologic(alteration_type)

    def test_create_model_alt_hydraulic_model_alt_hydraulic_created_with_correct_attributes(self):
        alteration_type = "zero_hydraulic"
        model_alt_hydraulic = self.model.create_model_alt_hydraulic(alteration_type)
        self.assertEquals(model_alt_hydraulic.model_alteration_type_id, 0)

    def test_create_model_alt_hydraulic_nonexistant_type_throws_exception(self):
        alteration_type = "type that does not exist"
        with self.assertRaises(KeyError):
            self.model.create_model_alt_hydraulic(alteration_type)

    def test_create_model_alterations_model_with_bc_category_alterations_list_has_correct_values(self):
        alteration_types = [["zero_bc"], ["one_bc"], ["two_bc"]]
        alteration_category = "bc"
        self.model.create_model_alterations(alteration_types, alteration_category)
        self.assertEquals(self.model.model_alterations[0].model_alteration_type_id, 0)
        self.assertEquals(self.model.model_alterations[1].model_alteration_type_id, 1)
        self.assertEquals(self.model.model_alterations[2].model_alteration_type_id, 2)

    def test_create_model_alterations_model_with_hydrologic_category_alterations_list_has_correct_values(self):
        alteration_types = [["zero_hydrologic"], ["one_hydrologic"], ["two_hydrologic"]]
        alteration_category = "hydrologic"
        self.model.create_model_alterations(alteration_types, alteration_category)
        self.assertEquals(self.model.model_alterations[0].model_alteration_type_id, 0)
        self.assertEquals(self.model.model_alterations[1].model_alteration_type_id, 1)
        self.assertEquals(self.model.model_alterations[2].model_alteration_type_id, 2)

    def test_create_model_alterations_model_with_hydraulic_category_alterations_list_has_correct_values(self):
        alteration_types = [["zero_hydraulic"], ["one_hydraulic"], ["two_hydraulic"]]
        alteration_category = "hydraulic"
        self.model.create_model_alterations(alteration_types, alteration_category)
        self.assertEquals(self.model.model_alterations[0].model_alteration_type_id, 0)
        self.assertEquals(self.model.model_alterations[1].model_alteration_type_id, 1)
        self.assertEquals(self.model.model_alterations[2].model_alteration_type_id, 2)

    def test_create_model_alterations_called_with_bc_category_calls_create_model_alt_bc(self):
        with mock.patch.object(self.model, "create_model_alt_bc") as mock_create_model_alt_bc:
            alteration_types = [["zero"], ["one"], ["two"]]
            alteration_category = "bc"
            self.model.create_model_alterations(alteration_types, alteration_category)
            self.assertTrue(mock_create_model_alt_bc.called)

    def test_create_model_alterations_called_with_hydrologic_category_calls_create_model_alt_hydrologic(self):
        with mock.patch.object(self.model, "create_model_alt_hydrologic") as mock_create_model_alt_hydrologic:
            alteration_types = [["zero"], ["one"], ["two"]]
            alteration_category = "hydrologic"
            self.model.create_model_alterations(alteration_types, alteration_category)
            self.assertTrue(mock_create_model_alt_hydrologic.called)

    def test_create_model_alterations_called_with_hydraulic_category_calls_create_model_alt_hydraulic(self):
        with mock.patch.object(self.model, "create_model_alt_hydraulic") as mock_create_model_alt_hydraulic:
            alteration_types = [["zero"], ["one"], ["two"]]
            alteration_category = "hydraulic"
            self.model.create_model_alterations(alteration_types, alteration_category)
            self.assertTrue(mock_create_model_alt_hydraulic.called)

    def test_create_model_alterations_bc_calls_create_model_alterations_with_correct_argument(self):
        with mock.patch.object(self.model, "create_model_alterations") as mock_create_model_alterations:
            alteration_types = [["zero"], ["one"], ["two"]]
            self.model.create_model_alterations_bc(alteration_types)
            mock_create_model_alterations.assert_called_with(alteration_types, "bc")

    def test_create_model_alterations_hydrologic_calls_create_model_alterations_with_correct_argument(self):
        with mock.patch.object(self.model, "create_model_alterations") as mock_create_model_alterations:
            alteration_types = [["zero"], ["one"], ["two"]]
            self.model.create_model_alterations_hydrologic(alteration_types)
            mock_create_model_alterations.assert_called_with(alteration_types, "hydrologic")

    def test_create_model_alterations_hydraulic_calls_create_model_alterations_with_correct_argument(self):
        with mock.patch.object(self.model, "create_model_alterations") as mock_create_model_alterations:
            alteration_types = [["zero"], ["one"], ["two"]]
            self.model.create_model_alterations_hydraulic(alteration_types)
            mock_create_model_alterations.assert_called_with(alteration_types, "hydraulic")

    # TODO: write tests to verify diagnostic tools report appropriate errors

    def test_valid_calibration_simulations_model_has_two_calibration_storms_returns_true(self):
        self.model.simulations = [self.mock_simulation1, self.mock_simulation2, self.mock_calibration_simulation1, self.mock_calibration_simulation2]
        is_valid = self.model.valid_calibration_simulations()
        self.assertTrue(is_valid)

    def test_valid_calibration_simulations_model_has_two_calibration_storms_with_invalid_desc_length_returns_false(self):
        self.mock_calibration_simulation1.sim_desc = "TAGD20190203"
        self.model.simulations = [self.mock_simulation1, self.mock_simulation2, self.mock_calibration_simulation1, self.mock_calibration_simulation2]
        is_valid = self.model.valid_calibration_simulations()
        self.assertFalse(is_valid)

    def test_valid_calibration_simulations_model_has_two_calibration_storms_with_invalid_desc_date_returns_false(self):
        self.mock_calibration_simulation1.sim_desc = "TAG20190250"
        self.model.simulations = [self.mock_simulation1, self.mock_simulation2, self.mock_calibration_simulation1, self.mock_calibration_simulation2]
        with self.assertRaises(InvalidCalibrationStormSimulationDescription):
            self.model.valid_calibration_simulations()

    def test_valid_calibration_simulations_model_has_two_calibration_storms_with_invalid_desc_string_in_date_returns_false(self):
        self.mock_calibration_simulation1.sim_desc = "TAG2019025O"
        self.model.simulations = [self.mock_simulation1, self.mock_simulation2, self.mock_calibration_simulation1, self.mock_calibration_simulation2]
        with self.assertRaises(InvalidCalibrationStormSimulationDescription):
            self.model.valid_calibration_simulations()

    def test_valid_calibration_simulations_model_has_no_calibration_storms_returns_false(self):
        self.model.simulations = [self.mock_simulation1, self.mock_simulation2]
        is_valid = self.model.valid_calibration_simulations()
        self.assertFalse(is_valid)

    def test_valid_ccsp_characterization_simulations_model_has_all_required_storms_returns_true(self):
        self.model.simulations = [self.mock_simulation1, self.mock_simulation2]
        is_valid = self.model.valid_ccsp_characterization_simulations()
        self.assertTrue(is_valid)