from unittest import TestCase
import mock
import os
import arcpy
from model_data_io import ModelDataIO
from model import Model
from simulation import Simulation
from config import Config


class TestModelDataIO(TestCase):

    def setUp(self):
        self.config = Config()
        self.modeldataio = ModelDataIO(self.config)
        self.mock_model = mock.MagicMock(Model)
        self.mock_model.model_path = r"C:\model_path"
        self.field_names = ["Model_ID", "Simulation_ID", "Storm_ID", "Dev_Scenario_ID", "Sim_Desc"]
        self.mock_simulation = mock.MagicMock(Simulation)
        self.mock_simulation.simulation_id = 22
        self.mock_simulation.storm_id = 33
        self.mock_simulation.dev_scenario_id = 44
        self.mock_simulation.sim_desc = "sim_desc"

    @mock.patch("os.walk")
    def test_read_simulations_calls_os_walk(self, mock_os_walk):

        self.modeldataio.read_simulations(self.mock_model)
        self.assertTrue(mock_os_walk.called)

    @mock.patch("os.walk")
    def test_read_simulation_reads_standard_simulation_existing_scenario_returns_simulation_object(self, mock_os_walk):

        mock_os_walk.return_value = iter([("path", ["D25yr6h"], "file name")])
        list_of_simulations = self.modeldataio.read_simulations(self.mock_model)
        first_simulation = list_of_simulations[0]  # type: Simulation
        self.assertEquals(first_simulation.model_path, r"C:\model_path")
        self.assertEquals(first_simulation.dev_scenario_id, 0)
        self.assertEquals(first_simulation.storm_id, 1)
        self.assertEquals(first_simulation.sim_desc, "D25yr6h")

    @mock.patch("os.walk")
    def test_read_simulation_reads_standard_simulation_build_out_scenario_returns_simulation_object(self, mock_os_walk):

        mock_os_walk.return_value = iter([("path", ["D25yr6h-BO"], "file name")])
        list_of_simulations = self.modeldataio.read_simulations(self.mock_model)
        first_simulation = list_of_simulations[0]  # type: Simulation
        self.assertEquals(first_simulation.model_path, r"C:\model_path")
        self.assertEquals(first_simulation.dev_scenario_id, 2)
        self.assertEquals(first_simulation.storm_id, 1)
        self.assertEquals(first_simulation.sim_desc, "D25yr6h-BO")

    @mock.patch("os.walk")
    def test_read_simulation_reads_list_of_simulations_and_returns_correct_simulation_objects(self, mock_os_walk):

        mock_os_walk.return_value = iter([("path", ["D25yr6h-BO","D10yr6h"], "file name")])
        list_of_simulations = self.modeldataio.read_simulations(self.mock_model)
        first_simulation = list_of_simulations[0]  # type: Simulation
        second_simulation = list_of_simulations[1]  # type: Simulation
        self.assertEquals(first_simulation.model_path, r"C:\model_path")
        self.assertEquals(first_simulation.dev_scenario_id, 2)
        self.assertEquals(first_simulation.storm_id, 1)
        self.assertEquals(first_simulation.sim_desc, "D25yr6h-BO")
        self.assertEquals(second_simulation.model_path, r"C:\model_path")
        self.assertEquals(second_simulation.dev_scenario_id, 0)
        self.assertEquals(second_simulation.storm_id, 2)
        self.assertEquals(second_simulation.sim_desc, "D10yr6h")

    @mock.patch("os.walk")
    def test_read_simulation_reads_user_defined_simulation_returns_simulation_object(self, mock_os_walk):

        mock_os_walk.return_value = iter([("path", ["Dec2015"], "file name")])
        list_of_simulations = self.modeldataio.read_simulations(self.mock_model)
        first_simulation = list_of_simulations[0]  # type: Simulation
        self.assertEquals(first_simulation.model_path, r"C:\model_path")
        self.assertEquals(first_simulation.dev_scenario_id, 0)
        self.assertEquals(first_simulation.storm_id, 0)
        self.assertEquals(first_simulation.sim_desc, "Dec2015")

    @mock.patch("arcpy.da.InsertCursor")
    def test_add_simulation_calls_insert_cursor(self, mock_insert_cursor):
        self.modeldataio.add_simulation("location", self.field_names, 11, self.mock_simulation)
        self.assertTrue(mock_insert_cursor.called)

    @mock.patch("arcpy.da.InsertCursor")
    def test_add_simulation_calls_insert_cursor_with_correct_arguments(self, mock_insert_cursor):
        self.modeldataio.add_simulation("location", self.field_names, 11, self.mock_simulation)
        mock_insert_cursor.assert_called_with("location", self.field_names)

    def test_add_simulation_parameters_are_passed_into_row(self):
        mock_cursor = mock.MagicMock(arcpy.da.InsertCursor)
        with mock.patch("arcpy.da.InsertCursor") as mock_da_InsertCursor:
            mock_da_InsertCursor.return_value = mock_cursor
            self.modeldataio.add_simulation("location", self.field_names, 11, self.mock_simulation)
        self.assertTrue(mock_cursor.insertRow.called)
        mock_cursor.insertRow.assert_called_with([11, 22, 33, 44, "sim_desc"])
