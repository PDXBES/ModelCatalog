from unittest import TestCase
from simulation import Simulation
import os
import mock


class TestSimulation(TestCase):
    def setUp(self):
        model_path = "String"
        self.simulation = Simulation(model_path)

    def test_simulation_is_valid(self):

        self.assertTrue(self.simulation.valid)




# TODO fix all this

    @mock.patch("os.path.exists")
    def test_has_results_check_sim_folder_has_results(self, mock_os_path_exists):
        self.simulation.has_results()
        self.assertTrue(mock_os_path_exists.called)

    @mock.patch("os.path.exists")
    def test_has_results_called_with_correct_arguments(self, mock_os_path_exists):
        self.simulation.storm = "D25yr6hr"
        self.simulation.scenario = "50"
        self.simulation.has_results()
        mock_os_path_exists.assert_called_with(self.simulation.model_path
                                               + "\\" + "sim\\"
                                               + self.simulation.storm
                                               + "-"
                                               + self.simulation.scenario
                                               + "\\results.gdb")

    @mock.patch("os.path.exists")
    def test_has_results_results_gdb_exists_return_true(self, mock_os_path_exists):
        mock_os_path_exists.return_value = True
        is_valid = self.simulation.has_results()
        self.assertTrue(is_valid)


    @mock.patch("os.path.exists")
    def test_has_results_results_gdb_does_not_exist_return_false(self, mock_os_path_exists):
        mock_os_path_exists.return_value = False
        is_valid = self.simulation.has_results()
        self.assertFalse(is_valid)

    def test_simulation_path_built(self):
        self.simulation.storm = "D25yr6hr"
        self.simulation.scenario = "50"
        sim_path = self.simulation.path()
        self.assertEquals(sim_path, self.simulation.model_path
                                               + "\\" + "sim\\"
                                               + self.simulation.storm
                                               + "-"
                                               + self.simulation.scenario)

