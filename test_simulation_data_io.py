from unittest import TestCase
import mock, arcpy
from simulation import Simulation
from model import Model
from simulation_data_io import SimulationDataIO


class TestSimulationDataIO(TestCase):
    def setUp(self):
        self.simulationdataio = SimulationDataIO()
        self.mock_simulation = mock.MagicMock(Simulation)
        self.mock_simulation.storm_id = 22
        self.mock_simulation.scenario_id = 33
        self.mock_model = mock.MagicMock(Model)
        self.mock_model.Model_ID = 1
        self.mock_search_cursor = [("a_value", "b_value")]
        self.mock_cursor = mock.MagicMock(arcpy.da.InsertCursor)
        self.mock_fields1 = mock.MagicMock(arcpy.Field)
        self.mock_fields2 = mock.MagicMock(arcpy.Field)
        self.mock_fields1.name = "a"
        self.mock_fields2.name = "b"
        self.patch_search_cursor = mock.patch("arcpy.da.SearchCursor")
        self.patch_insert_cursor = mock.patch("arcpy.da.InsertCursor")
        self.patch_list_fields = mock.patch("arcpy.ListFields")
        self.mock_list_fields = self.patch_list_fields.start()
        self.mock_da_SearchCursor = self.patch_search_cursor.start()
        self.mock_da_InsertCursor = self.patch_insert_cursor.start()
        self.mock_da_InsertCursor.return_value = self.mock_cursor
        self.mock_da_SearchCursor.return_value = self.mock_search_cursor
        self.mock_list_fields.return_value = [self.mock_fields1, self.mock_fields2]

    def tearDown(self):
        self.mock_list_fields = self.patch_list_fields.stop()
        self.mock_da_SearchCursor = self.patch_search_cursor.stop()
        self.mock_da_InsertCursor = self.patch_insert_cursor.stop()

    def test_copy_area_results_called_search_cursor(self):

        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        self.assertTrue(self.mock_da_SearchCursor.called)

# TODO - fix tests - mock field names - see None in line 37

    def test_copy_area_results_called_with_correct_arguments(self):
        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        results_path = self.mock_simulation.path() + "\\" + "results.gdb" + "\\" + "AreaResults"
        self.mock_da_SearchCursor.assert_called_with(results_path, ["a", "b"])

    def test_copy_area_results_called_insert_cursor(self):
        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        self.assertTrue(self.mock_da_InsertCursor.called)

    def test_copy_area_results_called_ListFields(self):
        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        self.assertTrue(self.mock_list_fields.called)

    def test_copy_area_results_added_four_new_fields_to_field_names(self):
        path = self.mock_simulation.path() + "\\" + "results.gdb" + "\\" + "AreaResults"
        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        self.mock_da_InsertCursor.assert_called_with(path, ["a", "b", "Model_ID", "Storm_ID", "Scenario_ID", "Is_Orphaned"])

    def test_copy_area_results_calls_insert_row_with_right_arguments(self):
        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        self.mock_cursor.insertRow.assert_called_with(('a_value', 'b_value', 1, 22, 33, 0))
