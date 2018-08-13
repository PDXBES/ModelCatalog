from unittest import TestCase
from simulation import Simulation
import mock
from config import Config

class TestSimulation(TestCase):
    def setUp(self):
        model_path = "String"
        self.config = Config()
        self.simulation = Simulation(model_path,self.config)
        self.simulation.storm_id = 1
        self.simulation.dev_scenario_id = 1

    @mock.patch("os.path.exists")
    def test_has_results_check_sim_folder_has_results(self, mock_os_path_exists):
        self.simulation.has_results()
        self.assertTrue(mock_os_path_exists.called)

    @mock.patch("os.path.exists")
    def test_has_results_called_with_correct_arguments_for_existing_scenario(self,
                                                       mock_os_path_exists):
        self.simulation.dev_scenario_id = 0
        self.simulation.has_results()
        path = "String" + "\\" + "sim\\" + "D25yr6h"
        mock_os_path_exists.assert_called_with(path)

    @mock.patch("os.path.exists")
    def test_has_results_called_with_correct_arguments_for_BO_scenario(self,
                                                       mock_os_path_exists):
        self.simulation.dev_scenario_id = 2
        self.simulation.has_results()
        path = "String" + "\\" + "sim\\" + "D25yr6h" + "-BO"
        mock_os_path_exists.assert_called_with(path)

    @mock.patch("os.path.exists")
    def test_has_results_results_gdb_exists_return_true(self,
                                                        mock_os_path_exists):
        mock_os_path_exists.return_value = True
        is_valid = self.simulation.has_results()
        self.assertTrue(is_valid)


    @mock.patch("os.path.exists")
    def test_has_results_results_gdb_does_not_exist_return_false(self, mock_os_path_exists):
        mock_os_path_exists.return_value = False
        is_valid = self.simulation.has_results()
        self.assertFalse(is_valid)

    def test_simulation_path_built_for_existing_scenario(self):
        self.simulation.dev_scenario_id = 0
        path = "String" + "\\" + "sim\\" + "D25yr6h" 
        sim_path = self.simulation.path()
        self.assertEquals(sim_path, path)

    def test_simulation_path_built_for_BO_scenario(self):
        self.simulation.dev_scenario_id = 2
        path = "String" + "\\" + "sim\\" + "D25yr6h" + "-BO"
        sim_path = self.simulation.path()
        self.assertEquals(sim_path, path)
    

