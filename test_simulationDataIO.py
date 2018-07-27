from unittest import TestCase
import mock
from simulation import Simulation
from Model import Model
from simulation_data_io import SimulationDataIO

class TestSimulationDataIO(TestCase):
    def setUp(self):
        self.simulationdataio = SimulationDataIO()
        self.mock_simulation = mock.MagicMock(Simulation)
        self.mock_model = mock.MagicMock(Model)

    @mock.patch("arcpy.da.InsertCursor")
    @mock.patch("arcpy.da.SearchCursor")
    @mock.patch("arcpy.ListFields")
    def test_copy_area_results_called_search_cursor(self, mock_list_fields, mock_da_SearchCursor, mock_da_InsertCursor):
        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        self.assertTrue(mock_da_SearchCursor.called)

    "TODO check that List fields called"
    "TODO check that List fields called with right arguments"
    "TODO make List fields return a list of fields and test " \
    "that insert_row setValue called with original  fields and four additional fields"

    #@mock.patch("arcpy.da.InsertCursor")
    #@mock.patch("arcpy.da.SearchCursor")
    #@mock.patch("arcpy.ListFields")


    @mock.patch("arcpy.da.InsertCursor")
    @mock.patch("arcpy.da.SearchCursor")
    @mock.patch("arcpy.ListFields")
    def test_copy_area_results_called_with_correct_arguments(self, mock_list_fields, mock_da_SearchCursor, mock_da_InsertCursor):
        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        results_path = self.mock_simulation.path() + "\\" + "results.gdb" + "\\" + "AreaResults"
        mock_da_SearchCursor.assert_called_with(results_path, None)

    @mock.patch("arcpy.da.InsertCursor")
    @mock.patch("arcpy.da.SearchCursor")
    @mock.patch("arcpy.ListFields")
    def test_copy_area_results_called_insert_cursor(self, mock_list_fields, mock_da_SearchCursor, mock_da_InsertCursor):
        self.simulationdataio.copy_area_results(self.mock_simulation.path())
        self.assertTrue(mock_da_InsertCursor.called)

    @mock.patch("arcpy.da.InsertCursor")
    @mock.patch("arcpy.da.SearchCursor")
    @mock.patch("arcpy.ListFields")
    def test_copy_area_results_called_ListFields(self, mock_list_fields, mock_da_SearchCursor, mock_da_InsertCursor):
        self.simulationdataio.copy_area_results(self.mock_simulation.path())
        self.assertTrue(mock_list_fields.called)

