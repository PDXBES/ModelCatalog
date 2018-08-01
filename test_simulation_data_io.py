from unittest import TestCase
import mock, arcpy
from simulation import Simulation
from model import Model
from simulation_data_io import SimulationDataIO


class TestSimulationDataIO(TestCase):
    def setUp(self):
        self.path = r"c:\temp\fake\sim\D25yr6h\results.gdb\AreaResults"
        self.simulationdataio = SimulationDataIO()

        self.patch_simulation_path = mock.patch("simulation.Simulation.path")
        self.mock_simulation_path = self.patch_simulation_path.start()
        self.mock_simulation_path.return_value = r"c:\temp\fake\sim\D25yr6h"

        self.mock_simulation = mock.MagicMock(Simulation)
        self.mock_simulation.storm = "D25yr6h"
        self.mock_simulation.scenario = ""
        self.mock_simulation.storm_id = 22
        self.mock_simulation.scenario_id = 33
        self.mock_model = mock.MagicMock(Model)
        self.mock_model.Model_Path = r"c:\temp\fake"
        self.mock_model.Model_ID = 1
        self.mock_search_cursor = [("a_value", "b_value")]
        self.mock_cursor = mock.MagicMock(arcpy.da.InsertCursor)
        self.mock_fields1 = mock.MagicMock(arcpy.Field)
        self.mock_fields2 = mock.MagicMock(arcpy.Field)
        self.mock_fields3 = mock.MagicMock(arcpy.Field)
        self.mock_fields4 = mock.MagicMock(arcpy.Field)
        self.mock_fields1.name = "a"
        self.mock_fields2.name = "b"
        self.mock_fields3.name = "SHAPE_Area"
        self.mock_fields4.name = "SHAPE_Length"
        self.patch_search_cursor = mock.patch("arcpy.da.SearchCursor")
        self.patch_insert_cursor = mock.patch("arcpy.da.InsertCursor")
        self.patch_list_fields = mock.patch("arcpy.ListFields")

        self.mock_list_fields = self.patch_list_fields.start()
        self.mock_da_SearchCursor = self.patch_search_cursor.start()
        self.mock_da_InsertCursor = self.patch_insert_cursor.start()
        self.mock_da_InsertCursor.return_value = self.mock_cursor
        self.mock_da_SearchCursor.return_value = self.mock_search_cursor
        self.mock_list_fields.return_value = [self.mock_fields1,
                                              self.mock_fields2,
                                              self.mock_fields3,
                                              self.mock_fields4]


    def tearDown(self):
        self.mock_list_fields = self.patch_list_fields.stop()
        self.mock_da_SearchCursor = self.patch_search_cursor.stop()
        self.mock_da_InsertCursor = self.patch_insert_cursor.stop()
        self.mock_simulation_path = self.patch_simulation_path.stop()

    def test_copy_area_results_called_search_cursor(self):

        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        self.assertTrue(self.mock_da_SearchCursor.called)

    def test_copy_area_results_called_with_correct_arguments(self):
        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        results_path = self.mock_simulation.path() + "\\" + "results.gdb" + "\\" + "AreaResults"
        self.mock_da_SearchCursor.assert_called_with(results_path, ["a", "b", "SHAPE@"])

    def test_copy_area_results_called_insert_cursor(self):
        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        self.assertTrue(self.mock_da_InsertCursor.called)

#    def test_copy_area_results_called_ListFields(self):
#        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
#        self.assertTrue(self.mock_list_fields.called)

    def test_copy_area_results_added_four_new_fields_to_field_names(self):
        area_results_path = '\\\\besfile1\\ccsp\\03_WP2_Planning_Support_Tools\\03_RRAD\\Model_Catalog\\Dev\\connection_files\\BESDBTEST1.RRAD_write.sde\\RRAD.GIS.AreaResults'
        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        self.mock_da_InsertCursor.assert_called_with(area_results_path, ["a", "b", "SHAPE@", "Model_ID", "Storm_ID", "Dev_Scenario_ID", "Is_Orphaned"])

    def test_copy_area_results_calls_insert_row_with_right_arguments(self):
        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        self.mock_cursor.insertRow.assert_called_with(('a_value', 'b_value', 1, 22, 33, 0))

    def test_modify_field_names_for_RRAD_called_list_fields(self):

        self.simulationdataio.modify_field_names_for_RRAD(self.path)
        self.assertTrue(self.mock_list_fields.called)

    def test_modify_field_names_for_RRAD_returns_correct_fields(self):
        field_names, field_names_extended = self.simulationdataio.modify_field_names_for_RRAD(self.path)
        self.assertEquals(field_names, ["a", "b", "SHAPE@"])
        self.assertEquals(field_names_extended, ["a", "b", "SHAPE@", "Model_ID", "Storm_ID", "Dev_Scenario_ID", "Is_Orphaned"])


# TODO fix this test
 #   def test_area_results_path_creates_correct_path(self):
 #       area_results_path = self.simulationdataio.area_results_path(self.mock_simulation)
 #       self.assertEquals(area_results_path, r"c:\temp\fake\sim\D25yr6h\results.gdb\AreaResults")
