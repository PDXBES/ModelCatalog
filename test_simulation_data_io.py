from unittest import TestCase
import mock, arcpy
from simulation import Simulation
from model import Model
from simulation_data_io import SimulationDataIO
from mock_config import MockConfig
from model_catalog_db_data_io import ModelCatalogDbDataIo


class TestSimulationDataIO(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        mock_model_catalog_db_data_io = mock.MagicMock(ModelCatalogDbDataIo)
        mock_model_catalog_db_data_io.config = self.config

        self.path = r"c:\temp\fake\sim\D25yr6h\results.gdb\AreaResults"
        self.simulationdataio = SimulationDataIO(self.config, mock_model_catalog_db_data_io)
        self.mock_simulation = mock.MagicMock(Simulation)
        self.mock_simulation.storm = "D25yr6h"
        self.mock_simulation.scenario = ""
        self.mock_simulation.storm_id = 22
        self.mock_simulation.dev_scenario_id = 33
        self.mock_model = mock.MagicMock(Model)
        self.simulation = Simulation(self.mock_model, self.config)
        self.mock_model.model_path = r"c:\temp\fake"
        self.mock_model.id = 1
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

    def test_copy_feature_class_results_called_search_cursor(self):
        rrad_results_feature_class_path = "insert rrad path here"
        model_results_feature_class_path = "this is a test string"
        self.simulationdataio.copy_feature_class_results(self.mock_simulation,
                                                         self.mock_model,
                                                         model_results_feature_class_path,
                                                         rrad_results_feature_class_path)
        self.assertTrue(self.mock_da_SearchCursor.called)

    def test_copy_feature_class_results_called_with_correct_arguments(self):
        rrad_results_feature_class_path = "insert rrad path here"
        model_results_feature_class_path = "this is a test string"
        self.simulationdataio.copy_feature_class_results(self.mock_simulation,
                                                         self.mock_model,
                                                         model_results_feature_class_path,
                                                         rrad_results_feature_class_path)
        self.mock_da_SearchCursor.assert_called_with(model_results_feature_class_path, ["a", "b", "SHAPE@"])

    def test_copy_feature_class_results_called_insert_cursor(self):
        rrad_results_feature_class_path = "insert rrad path here"
        model_results_feature_class_path = "this is a test string"
        self.simulationdataio.copy_feature_class_results(self.mock_simulation,
                                                         self.mock_model,
                                                         model_results_feature_class_path,
                                                         rrad_results_feature_class_path)
        self.assertTrue(self.mock_da_InsertCursor.called)

#    def test_copy_area_results_called_ListFields(self):
#        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
#        self.assertTrue(self.mock_list_fields.called)

    def test_copy_feature_class_results_added_four_new_fields_to_field_names(self):
        rrad_results_feature_class_path = "insert rrad path here"
        model_results_feature_class_path = "this is a test string"
        self.simulationdataio.copy_feature_class_results(self.mock_simulation,
                                                         self.mock_model,
                                                         model_results_feature_class_path,
                                                         rrad_results_feature_class_path)
        self.mock_da_InsertCursor.assert_called_with(rrad_results_feature_class_path, ["a", "b", "SHAPE@", "Model_ID", "Storm_ID", "Dev_Scenario_ID", "Is_Orphaned"])

    def test_copy_feature_class_results_calls_insert_row_with_right_arguments(self):
        rrad_results_feature_class_path = "insert rrad path here"
        model_results_feature_class_path = "this is a test string"
        self.simulationdataio.copy_feature_class_results(self.mock_simulation,
                                                         self.mock_model,
                                                         model_results_feature_class_path,
                                                         rrad_results_feature_class_path)
        self.mock_cursor.insertRow.assert_called_with(('a_value', 'b_value', 1, 22, 33, 0))

    def test_modify_field_names_for_RRAD_called_list_fields(self):

        self.simulationdataio.modify_field_names_for_RRAD(self.path)
        self.assertTrue(self.mock_list_fields.called)

    def test_modify_field_names_for_RRAD_returns_correct_fields(self):
        field_names, field_names_extended = self.simulationdataio.modify_field_names_for_RRAD(self.path)
        self.assertEquals(field_names, ["a", "b", "SHAPE@"])
        self.assertEquals(field_names_extended, ["a", "b", "SHAPE@", "Model_ID", "Storm_ID", "Dev_Scenario_ID", "Is_Orphaned"])

    @mock.patch("simulation.Simulation.path")
    def test_area_results_path_creates_correct_path(self, mock_simulation_path):
        mock_simulation_path.return_value = r"c:\temp\fake\sim\D25yr6h"
        area_results_path = self.simulationdataio.area_results_path(self.simulation)
        self.assertEquals(area_results_path, r"c:\temp\fake\sim\D25yr6h\results.gdb\AreaResults")

    @mock.patch("simulation.Simulation.path")
    def test_link_results_path_creates_correct_path(self, mock_simulation_path):
        mock_simulation_path.return_value = r"c:\temp\fake\sim\D25yr6h"
        link_results_path = self.simulationdataio.link_results_path(self.simulation)
        self.assertEquals(link_results_path, r"c:\temp\fake\sim\D25yr6h\results.gdb\LinkResults")

    @mock.patch("simulation.Simulation.path")
    def test_node_results_path_creates_correct_path(self, mock_simulation_path):
        mock_simulation_path.return_value = r"c:\temp\fake\sim\D25yr6h"
        node_results_path = self.simulationdataio.node_results_path(self.simulation)
        self.assertEquals(node_results_path, r"c:\temp\fake\sim\D25yr6h\results.gdb\NodeResults")

    @mock.patch("simulation.Simulation.path")
    def test_node_flooding_results_path_creates_correct_path(self, mock_simulation_path):
        mock_simulation_path.return_value = r"c:\temp\fake\sim\D25yr6h"
        node_flooding_results_path = self.simulationdataio.node_flooding_results_path(self.simulation)
        self.assertEquals(node_flooding_results_path, r"c:\temp\fake\sim\D25yr6h\results.gdb\NodeFloodingResults")

    @mock.patch("simulation_data_io.SimulationDataIO.copy_feature_class_results")
    def test_copy_area_results_copy_feature_class_results_is_called(self, mock_copy_feature_class_results):
        self.simulationdataio.copy_area_results(self.mock_simulation, self.mock_model)
        mock_copy_feature_class_results.assert_called()

    @mock.patch("simulation_data_io.SimulationDataIO.copy_feature_class_results")
    @mock.patch("simulation.Simulation.path")
    def test_copy_area_results_copy_feature_class_results_is_called_with_correct_argments(self,
                                                                                          mock_simulation_path,
                                                                                          mock_copy_feature_class_results):
        simulation_path = r"c:\temp\fake\sim\D25yr6h"
        model_area_results_path = simulation_path + "\\" + "results.gdb" + "\\" + "AreaResults"
        mock_simulation_path.return_value = simulation_path
        rrad_area_results_path = self.config.area_results_sde_path
        self.simulationdataio.copy_area_results(self.simulation, self.mock_model)
        mock_copy_feature_class_results.assert_called_with(self.simulation,
                                                           self.mock_model,
                                                           model_area_results_path,
                                                           rrad_area_results_path)

#TODO: Write new tests( copy function called, called with correct args) for copy link results due to new copy function