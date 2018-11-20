from unittest import TestCase
import mock
import arcpy
from model_data_io import ModelDataIo
from model import Model
from simulation import Simulation
from model_catalog_db_data_io import ModelCatalogDbDataIo
from mock_config import MockConfig
from model_alteration import ModelAlteration
from model_alt_bc import ModelAltBC
from model_alt_hydrologic import ModelAltHydrologic
from model_alt_hydraulic import ModelAltHydraulic
from collections import OrderedDict
from project_type import ProjectType

class TestModelDataIO(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.model_catalog_data_io = ModelCatalogDbDataIo(self.config)
        self.model_data_io = ModelDataIo(self.config, self.model_catalog_data_io)
        self.field_names = ["Model_ID", "Simulation_ID", "Storm_ID", "Dev_Scenario_ID", "Sim_Desc"]

        self.mock_model_alt_bc = mock.MagicMock(ModelAltBC)
        self.mock_model_alt_hydrologic = mock.MagicMock(ModelAltHydrologic)
        self.mock_model_alt_hydraulic = mock.MagicMock(ModelAltHydraulic)
        self.generic_field_attribute_lookup = OrderedDict()
        self.generic_field_attribute_lookup["Generic_ID"] = "id"
        self.generic_field_attribute_lookup["Generic_Domain_ID"] = "generic_domain_id"

        self.mock_model_alt_bc.field_attribute_lookup = self.generic_field_attribute_lookup
        self.mock_model_alt_bc.name = "model_alt_bc"
        self.mock_model_alt_hydrologic.field_attribute_lookup = self.generic_field_attribute_lookup
        self.mock_model_alt_hydrologic.name = "model_alt_hydrologic"
        self.mock_model_alt_hydraulic.field_attribute_lookup = self.generic_field_attribute_lookup
        self.mock_model_alt_hydraulic.name = "model_alt_hydraulic"

        self.mock_simulation = mock.MagicMock(Simulation)
        self.mock_simulation.simulation_id = 22
        self.mock_simulation.storm_id = 33
        self.mock_simulation.dev_scenario_id = 44
        self.mock_simulation.sim_desc = "sim_desc"
        self.mock_simulation.config = self.config
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup[0] = ["Model_ID", "parent_id"]
        field_attribute_lookup[1] = ["Simulation_ID", "id"]
        field_attribute_lookup[2] = ["Storm_ID", "storm_id"]
        field_attribute_lookup[3] = ["Dev_Scenario_ID", "dev_scenario_id"]
        field_attribute_lookup[4] = ["Sim_Desc", "sim_desc"]
        self.mock_simulation.field_attribute_lookup = field_attribute_lookup

        self.mock_project_type = mock.MagicMock(ProjectType)
        self.mock_project_type.field_attribute_lookup = self.generic_field_attribute_lookup

        self.mock_model = mock.MagicMock(Model)
        self.mock_model.model_path = r"C:\model_path"
        self.mock_model.id = 11
        self.mock_model.valid = True
        self.mock_model.simulations = [self.mock_simulation]
        self.mock_model.project_types = [self.mock_project_type]

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

        self.patch_retrieve_current_simulation_id = mock.patch("model_catalog_db_data_io.ModelCatalogDbDataIo.retrieve_current_simulation_id")
        self.mock_retrieve_current_simulation_id = self.patch_retrieve_current_simulation_id.start()
        self.mock_retrieve_current_simulation_id.return_value = 1

        self.patch_add_object = mock.patch.object(self.model_data_io, "add_object")
        self.mock_add_object = self.patch_add_object.start()

        self.mock_model.simulations = [self.mock_simulation]
        self.mock_model.model_alterations = [self.mock_model_alt_bc]


    def tearDown(self):
        self.mock_dissolve = self.patch_dissolve.stop()
        self.mock_insert_cursor = self.patch_insert_cursor.stop()
        self.mock_search_cursor = self.patch_search_cursor.stop()
        self.mock_retrieve_current_simulation_id = self.patch_retrieve_current_simulation_id.stop()
        self.mock_add_object = self.patch_add_object.stop()

    @mock.patch("os.walk")
    def test_read_simulations_calls_os_walk(self, mock_os_walk):
        self.model_data_io.read_simulations(self.mock_model)
        self.assertTrue(mock_os_walk.called)

    @mock.patch("os.walk")
    def test_read_simulation_reads_standard_simulation_existing_scenario_returns_simulation_object(self, mock_os_walk):
        mock_os_walk.return_value = iter([("path", ["D25yr6h"], "file name")])
        list_of_simulations = self.model_data_io.read_simulations(self.mock_model)
        first_simulation = list_of_simulations[0]  # type: Simulation
        self.assertEquals(first_simulation.model_path, r"C:\model_path")
        self.assertEquals(first_simulation.dev_scenario_id, 0)
        self.assertEquals(first_simulation.storm_id, 1)
        self.assertEquals(first_simulation.sim_desc, "D25yr6h")

    @mock.patch("os.walk")
    def test_read_simulation_reads_standard_simulation_build_out_scenario_returns_simulation_object(self, mock_os_walk):
        mock_os_walk.return_value = iter([("path", ["D25yr6h-BO"], "file name")])
        list_of_simulations = self.model_data_io.read_simulations(self.mock_model)
        first_simulation = list_of_simulations[0]  # type: Simulation
        self.assertEquals(first_simulation.model_path, r"C:\model_path")
        self.assertEquals(first_simulation.dev_scenario_id, 2)
        self.assertEquals(first_simulation.storm_id, 1)
        self.assertEquals(first_simulation.sim_desc, "D25yr6h-BO")

    @mock.patch("os.walk")
    def test_read_simulation_reads_list_of_simulations_and_returns_correct_simulation_objects(self, mock_os_walk):
        mock_os_walk.return_value = iter([("path", ["D25yr6h-BO","D10yr6h"], "file name")])
        list_of_simulations = self.model_data_io.read_simulations(self.mock_model)
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
        list_of_simulations = self.model_data_io.read_simulations(self.mock_model)
        first_simulation = list_of_simulations[0]  # type: Simulation
        self.assertEquals(first_simulation.model_path, r"C:\model_path")
        self.assertEquals(first_simulation.dev_scenario_id, 0)
        self.assertEquals(first_simulation.storm_id, 0)
        self.assertEquals(first_simulation.sim_desc, "Dec2015")

    def test_add_simulation_calls_add_object(self):
        self.model_data_io.add_simulation(11, self.mock_simulation)
        self.assertTrue(self.mock_add_object.called)

    def test_add_simulation_calls_add_object_with_correct_arguments(self):
        self.model_data_io.add_simulation(11, self.mock_simulation)
        self.mock_add_object.assert_called_with(11, self.mock_simulation, self.mock_simulation.field_attribute_lookup,
                                                self.config.simulation_sde_path)

    def test_create_model_geometry_calls_arcpy_dissolve_management(self):
        self.model_data_io.create_model_geometry(self.mock_model)
        self.assertTrue(self.mock_dissolve.called)

    def test_create_model_geometry_calls_arcpy_dissolve_management_with_the_correct_arguments(self):
        self.model_data_io.create_model_geometry(self.mock_model)
        input = "C:\model_path" + "\\" + "EmgaatsModel.gdb" + "\\Network\\Links"
        self.mock_dissolve.assert_called_with(input, "in_memory\\Links", "", "", "MULTI_PART")

    def test_create_model_geometry_calls_search_cursor(self):
        self.model_data_io.create_model_geometry(self.mock_model)
        self.assertTrue(self.mock_search_cursor.called)

    def test_create_model_geometry_calls_search_cursor_with_correct_arguments(self):
        self.model_data_io.create_model_geometry(self.mock_model)
        self.mock_search_cursor.assert_called_with( "in_memory\\Links" , ["Shape@"])

    def test_create_model_geometry_invalid_model_returns_exception(self):
        self.mock_model.model_geometry = None
        self.model_data_io.create_model_geometry(self.mock_model)
        self.assertEqual(self.mock_model.model_geometry, "geom")

    def test_add_model_alteration_called_with_alt_bc_calls_add_object_with_correct_arguments(self):
        with mock.patch.object(self.model_data_io, "add_object") as mock_add_object:
            self.model_data_io.add_model_alteration(11, self.mock_model_alt_bc)
            mock_add_object.assert_called_with(11, self.mock_model_alt_bc,
                                               self.generic_field_attribute_lookup,
                                               self.config.model_alt_bc_sde_path)

    def test_add_model_alteration_called_with_alt_hydrologic_calls_add_object_with_correct_arguments(self):
        with mock.patch.object(self.model_data_io, "add_object") as mock_add_object:
            self.model_data_io.add_model_alteration(11, self.mock_model_alt_hydrologic)
            mock_add_object.assert_called_with(11, self.mock_model_alt_hydrologic,
                                               self.generic_field_attribute_lookup,
                                               self.config.model_alt_hydrologic_sde_path)

    def test_add_model_alteration_called_with_alt_hydraulic_calls_add_object_with_correct_arguments(self):
        with mock.patch.object(self.model_data_io, "add_object") as mock_add_object:
            self.model_data_io.add_model_alteration(11, self.mock_model_alt_hydraulic)
            mock_add_object.assert_called_with(11, self.mock_model_alt_hydraulic,
                                               self.generic_field_attribute_lookup,
                                               self.config.model_alt_hydraulic_sde_path)

    def test_add_simulations_calls_add_simulation(self):
        patch_add_simulation = mock.patch.object(self.model_data_io, "add_simulation")
        mock_add_simulation = patch_add_simulation.start()
        self.model_data_io.add_simulations(self.mock_model)
        self.assertTrue(mock_add_simulation.called)
        patch_add_simulation.stop()

    def test_add_simulations_calls_add_simulation_with_correct_arguments(self):
        patch_add_simulation = mock.patch.object(self.model_data_io, "add_simulation")
        mock_add_simulation = patch_add_simulation.start()
        self.model_data_io.add_simulations(self.mock_model)
        mock_add_simulation.assert_called_with(11, self.mock_simulation)
        patch_add_simulation.stop()

    def test_add_model_alterations_calls_add_model_alteration(self):
        patch_add_model_alteration = mock.patch.object(self.model_data_io, "add_model_alteration")
        mock_add_model_alteration = patch_add_model_alteration.start()
        self.model_data_io.add_model_alterations(self.mock_model)
        self.assertTrue(mock_add_model_alteration.called)
        patch_add_model_alteration.stop()

    def test_add_model_alterations_calls_add_model_alteration_with_correct_arguments(self):
        patch_add_model_alteration = mock.patch.object(self.model_data_io, "add_model_alteration")
        mock_add_model_alteration = patch_add_model_alteration.start()
        self.model_data_io.add_model_alterations(self.mock_model)
        mock_add_model_alteration.assert_called_with(11, self.mock_model_alt_bc)
        patch_add_model_alteration.stop()

    def test_add_project_type_calls_add_object(self):
        with mock.patch.object(self.model_data_io, "add_object") as mock_add_object:
            self.model_data_io.add_project_type(11, self.mock_project_type)
            self.assertTrue(mock_add_object.called)

    def test_add_project_type_calls_add_object_with_correct_arguments(self):
        with mock.patch.object(self.model_data_io, "add_object") as mock_add_object:
            self.model_data_io.add_project_type(11, self.mock_project_type)
            mock_add_object.assert_called_with(11, self.mock_project_type,
                                               self.generic_field_attribute_lookup, self.config.project_type_sde_path)

    def test_add_project_types_calls_add_project_type(self):
        patch_add_project_type = mock.patch.object(self.model_data_io, "add_project_type")
        mock_add_project_type = patch_add_project_type.start()
        self.model_data_io.add_project_types(self.mock_model)
        self.assertTrue(mock_add_project_type.called)
        patch_add_project_type.stop()

    def test_add_project_types_calls_add_project_type_with_correct_arguments(self):
        patch_add_project_type = mock.patch.object(self.model_data_io, "add_project_type")
        mock_add_project_type = patch_add_project_type.start()
        self.model_data_io.add_project_types(self.mock_model)
        mock_add_project_type.assert_called_with(11, self.mock_project_type)
        patch_add_project_type.stop()
