from unittest import TestCase
import mock
import arcpy
from model_data_io import ModelDataIo
from model import Model
from simulation import Simulation
from model_catalog_data_io import ModelCatalogDbDataIo
from mock_config import MockConfig
from config import Config
from model_alteration import ModelAlteration

class TestModelDataIO(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.modeldataio = ModelDataIo(self.config)
        self.model_catalog_data_io = ModelCatalogDbDataIo(self.config)
        self.field_names = ["Model_ID", "Simulation_ID", "Storm_ID", "Dev_Scenario_ID", "Sim_Desc"]
        self.mock_model_alteration = mock.MagicMock(ModelAlteration)
        self.mock_simulation = mock.MagicMock(Simulation)
        self.mock_simulation.simulation_id = 22
        self.mock_simulation.storm_id = 33
        self.mock_simulation.dev_scenario_id = 44
        self.mock_simulation.sim_desc = "sim_desc"
        self.mock_simulation.config = self.config
        self.mock_model = mock.MagicMock(Model)
        self.mock_model.model_path = r"C:\model_path"
        self.mock_model.id = 11
        self.mock_model.valid = True
        self.mock_model.simulations = [self.mock_simulation]

        self.mock_insert_cursor_object = mock.MagicMock(arcpy.da.InsertCursor)
        self.mock_search_cursor_object = mock.MagicMock(arcpy.da.SearchCursor)
        self.mock_search_cursor_object.__iter__.return_value = iter([["geom"]])

        self.patch_dissolve = mock.patch("arcpy.Dissolve_management")
        self.mock_dissolve = self.patch_dissolve.start()

        self.patch_insert_cursor = mock.patch("arcpy.da.InsertCursor")
        self.mock_insert_cursor = self.patch_insert_cursor.start()

        self.patch_search_cursor = mock.patch("arcpy.da.SearchCursor")
        self.mock_search_cursor = self.patch_search_cursor.start()
        self.mock_search_cursor.return_value = self.mock_search_cursor_object

    def tearDown(self):
        self.mock_dissolve = self.patch_dissolve.stop()
        self.mock_insert_cursor = self.patch_insert_cursor.stop()
        self.mock_search_cursor = self.patch_search_cursor.stop()

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

    @mock.patch("model_catalog_data_io.ModelCatalogDbDataIo.retrieve_current_simulation_id")
    def test_add_simulation_calls_insert_cursor(self, mock_retrieve_current_simulation_id):
        mock_retrieve_current_simulation_id.return_value = 1
        self.modeldataio.add_simulation(11, self.mock_simulation, self.model_catalog_data_io)
        self.assertTrue(self.mock_insert_cursor.called)

    @mock.patch("model_catalog_data_io.ModelCatalogDbDataIo.retrieve_current_simulation_id")
    def test_add_simulation_calls_insert_cursor_with_correct_arguments(self, mock_retrieve_current_simulation_id):
        mock_retrieve_current_simulation_id.return_value = 1
        self.modeldataio.add_simulation(11, self.mock_simulation, self.model_catalog_data_io)
        self.mock_insert_cursor.assert_called_with(self.config.simulation_sde_path, self.field_names)

    @mock.patch("model_catalog_data_io.ModelCatalogDbDataIo.retrieve_current_simulation_id")
    def test_add_simulation_parameters_are_passed_into_row(self, mock_retrieve_current_simulation):
        mock_retrieve_current_simulation.return_value = 22
        self.mock_insert_cursor.return_value = self.mock_insert_cursor
        self.modeldataio.add_simulation(11, self.mock_simulation, self.model_catalog_data_io)
        self.assertTrue(self.mock_insert_cursor.insertRow.called)
        self.mock_insert_cursor.insertRow.assert_called_with([11, 22, 33, 44, "sim_desc"])

    @mock.patch("model_catalog_data_io.ModelCatalogDbDataIo.retrieve_current_simulation_id")
    @mock.patch("model_data_io.ModelDataIO.add_simulation")
    def test_add_simulations_called_with_correct_arguments(self, mock_add_simulation,
                                                           mock_retrieve_current_simulation):
        mock_retrieve_current_simulation.return_value = 22
        self.mock_insert_cursor .return_value = self.mock_insert_cursor_object
        self.modeldataio.add_simulations(self.mock_model, self.model_catalog_data_io)
        mock_add_simulation.assert_called_with(11, self.mock_model.simulations[0], self.model_catalog_data_io)

    def test_create_model_geometry_calls_arcpy_dissolve_management(self):
        self.modeldataio.create_model_geometry(self.mock_model)
        self.assertTrue(self.mock_dissolve.called)

    def test_create_model_geometry_calls_arcpy_dissolve_management_with_the_correct_arguments(self):
        self.modeldataio.create_model_geometry(self.mock_model)
        input = "C:\model_path" + "\\" + "EmgaatsModel.gdb" + "\\Network\\Links"
        self.mock_dissolve.assert_called_with(input, "in_memory\\Links", "", "", "MULTI_PART")

    def test_create_model_geometry_calls_search_cursor(self):
        self.modeldataio.create_model_geometry(self.mock_model)
        self.assertTrue(self.mock_search_cursor.called)

    def test_create_model_geometry_calls_search_cursor_with_correct_arguments(self):
        self.modeldataio.create_model_geometry(self.mock_model)
        self.mock_search_cursor.assert_called_with( "in_memory\\Links" , ["Shape@"])

    def test_create_model_geometry_invalid_model_returns_exception(self):
        self.mock_model.model_geometry = None
        self.modeldataio.create_model_geometry(self.mock_model)
        self.assertEqual(self.mock_model.model_geometry, "geom")



    def test_add_model_alteration_calls_add_object(self):
        with mock.patch.object(self.modeldataio, "add_object") as mock_add_object:
            self.modeldataio.add_model_alteration(self.mock_model_alteration)
            self.assertTrue(mock_add_object.called)