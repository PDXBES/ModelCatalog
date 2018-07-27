from unittest import TestCase
from Model import Model
from simulation import Simulation
import mock
from modelCatalog_exception import Invalid_model_path_exception


class TestModel(TestCase):

    def setUp(self):
        self.model = Model()
        self.model.Model_Path = r"c:\temp"

    @mock.patch("os.path.exists")
    def test_validate_model_path_check_path_exists_called(self, mock_os_path_exists):
        self.model.validate_model_path()
        self.assertTrue(mock_os_path_exists.called)

    @mock.patch("os.path.exists")
    def test_validate_model_path_called_with_correct_arguments(self, mock_os_path_exists):
        self.model.validate_model_path()
        mock_os_path_exists.assert_called_with(self.model.Model_Path)

    @mock.patch("os.path.exists")
    def test_validate_model_path_check_for_valid_path_if_valid_return_true(self, mock_os_path_exists):
        self.model.validate_model_path()
        self.assertTrue(mock_os_path_exists.called)

    @mock.patch("os.path.exists")
    def test_validate_model_path_check_for_valid_path_if_invalid_return_false(self, mock_os_path_exists):
        mock_os_path_exists.return_value = False
        is_valid = self.model.validate_model_path()
        self.assertEqual(is_valid, False)

    @mock.patch("os.path.isfile")
    def test_validate_config_file_check_config_file_exists(self, mock_os_path_isfile):
        self.model.validate_config_file()
        self.assertTrue(mock_os_path_isfile.called)

    @mock.patch("os.path.isfile")
    def test_validate_config_file_called_with_correct_arguments(self, mock_os_path_isfile):
        self.model.validate_config_file()
        mock_os_path_isfile.assert_called_with(self.model.Model_Path + "\\" + "emgaats.config")

    @mock.patch("os.path.isfile")
    def test_validate_config_file_if_config_file_exists_return_true(self,mock_os_path_isfile):
        mock_os_path_isfile.return_value = True
        is_valid = self.model.validate_config_file()
        self.assertTrue(is_valid)

    @mock.patch("os.path.isfile")
    def test_validate_config_file_if_config_file_does_not_exist_return_false(self,mock_os_path_isfile):
        mock_os_path_isfile.return_value = False
        is_valid = self.model.validate_config_file()
        self.assertEqual(is_valid, False)

    #TODO check that config file has valid values for ExtractionDateTime, ExtractionOriginalPath, EmgaatsVersion

    @mock.patch("os.path.exists")
    def test_validate_gdb_check_gdb_exists(self, mock_os_path_exists):
        self.model.validate_gdb()
        self.assertTrue(mock_os_path_exists.called)

    @mock.patch("os.path.exists")
    def test_validate_gdb_called_with_correct_arguments(self, mock_os_path_exists):
        self.model.validate_gdb()
        mock_os_path_exists.assert_called_with(self.model.Model_Path + "\\" + "EmgaatsModel.gdb")

    @mock.patch("os.path.exists")
    def test_validate_gdb_gdb_exists_return_true(self,mock_os_path_exists):
        mock_os_path_exists.return_value = True
        is_valid = self.model.validate_gdb()
        self.assertTrue(is_valid)

    @mock.patch("os.path.exists")
    def test_validate_gdb_gdb_file_does_not_exist_return_false(self,mock_os_path_exists):
        mock_os_path_exists.return_value = False
        is_valid = self.model.validate_gdb()
        self.assertEqual(is_valid, False)

    @mock.patch("os.path.exists")
    def test_validate_sim_check_sim_folder_exists(self, mock_os_path_exists):
        self.model.validate_sim()
        self.assertTrue(mock_os_path_exists.called)

    @mock.patch("os.path.exists")
    def test_validate_sim_called_with_correct_arguments(self, mock_os_path_exists):
        self.model.validate_sim()
        mock_os_path_exists.assert_called_with(self.model.Model_Path + "\\" + "sim")

    @mock.patch("os.path.exists")
    def test_validate_sim_sim_folder_exists_return_true(self, mock_os_path_exists):
        mock_os_path_exists.return_value = True
        is_valid = self.model.validate_sim()
        self.assertTrue(is_valid)

    @mock.patch("os.path.exists")
    def test_validate_sim_sim_folder_does_not_exist_return_false(self, mock_os_path_exists):
        mock_os_path_exists.return_value = False
        is_valid = self.model.validate_sim()
        self.assertEqual(is_valid, False)

    #TODO Write tests to for method to check for simulations

    #TODO Troubleshoot following test

    @mock.patch("Model.Model.validate_model_path")
    @mock.patch("Model.Model.validate_config_file")
    @mock.patch("Model.Model.validate_gdb")
    @mock.patch("Model.Model.validate_sim")
    def test_valid_if_model_path_config_gdb_and_sim_are_valid_return_true(self, mock_validate_sim, mock_validate_gdb,
                                                   mock_validate_config_file, mock_validate_model_path):
        mock_validate_sim.return_value = True
        mock_validate_gdb.return_value = True
        mock_validate_config_file.return_value = True
        mock_validate_model_path.return_value = True
        is_valid = self.model.valid
        self.assertTrue(is_valid)

    @mock.patch("Model.Model.validate_model_path")
    @mock.patch("Model.Model.validate_config_file")
    @mock.patch("Model.Model.validate_gdb")
    @mock.patch("Model.Model.validate_sim")
    def test_valid_if_model_path_invalid_return_false(self, mock_validate_sim, mock_validate_gdb,
                                                   mock_validate_config_file, mock_validate_model_path):
        mock_validate_sim.return_value = True
        mock_validate_gdb.return_value = True
        mock_validate_config_file.return_value = True
        mock_validate_model_path.return_value = False
        is_valid = self.model.valid
        self.assertFalse(is_valid)

    @mock.patch("Model.Model.validate_model_path")
    @mock.patch("Model.Model.validate_config_file")
    @mock.patch("Model.Model.validate_gdb")
    @mock.patch("Model.Model.validate_sim")
    def test_valid_if_model_config_invalid_return_false(self, mock_validate_sim, mock_validate_gdb,
                                                   mock_validate_config_file, mock_validate_model_path):
        mock_validate_sim.return_value = True
        mock_validate_gdb.return_value = True
        mock_validate_config_file.return_value = False
        mock_validate_model_path.return_value = True
        is_valid = self.model.valid
        self.assertFalse(is_valid)

    @mock.patch("Model.Model.validate_model_path")
    @mock.patch("Model.Model.validate_config_file")
    @mock.patch("Model.Model.validate_gdb")
    @mock.patch("Model.Model.validate_sim")
    def test_valid_if_gdb_invalid_return_false(self, mock_validate_sim, mock_validate_gdb,
                                                   mock_validate_config_file, mock_validate_model_path):
        mock_validate_sim.return_value = True
        mock_validate_gdb.return_value = False
        mock_validate_config_file.return_value = True
        mock_validate_model_path.return_value = True
        is_valid = self.model.valid
        self.assertFalse(is_valid)

    @mock.patch("Model.Model.validate_model_path")
    @mock.patch("Model.Model.validate_config_file")
    @mock.patch("Model.Model.validate_gdb")
    @mock.patch("Model.Model.validate_sim")
    def test_valid_if_sim_invalid_return_false(self, mock_validate_sim, mock_validate_gdb,
                                                   mock_validate_config_file, mock_validate_model_path):
        mock_validate_sim.return_value = False
        mock_validate_gdb.return_value = True
        mock_validate_config_file.return_value = True
        mock_validate_model_path.return_value = True
        is_valid = self.model.valid
        self.assertFalse(is_valid)

    @mock.patch("Model.Model.validate_model_path")
    @mock.patch("Model.Model.validate_config_file")
    @mock.patch("Model.Model.validate_gdb")
    @mock.patch("Model.Model.validate_sim")
    def test_valid_if_all_invalid_return_false(self, mock_validate_sim, mock_validate_gdb,
                                                   mock_validate_config_file, mock_validate_model_path):
        mock_validate_sim.return_value = False
        mock_validate_gdb.return_value = False
        mock_validate_config_file.return_value = False
        mock_validate_model_path.return_value = False
        is_valid = self.model.valid
        self.assertFalse(is_valid)

    def test_model_has_simulations(self):
        simulation = Simulation()
        self.model.simulations.append(simulation)
        self.assertTrue(len(self.model.simulations) > 0 )

    def test_first_simulation_is_valid(self):
        sim_one = self.model.simulations[0]

        self.assertTrue(sim_one)


