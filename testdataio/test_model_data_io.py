from unittest import TestCase
import mock
import arcpy
import json
from stat import S_IREAD, S_IRGRP, S_IROTH
from dataio.model_data_io import ModelDataIo
from businessclasses.model import Model
from businessclasses.simulation import Simulation
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from testbusinessclasses.mock_config import MockConfig
from businessclasses.model_alt_bc import ModelAltBc
from businessclasses.model_alt_hydrologic import ModelAltHydrologic
from businessclasses.model_alt_hydraulic import ModelAltHydraulic
from collections import OrderedDict
from businessclasses.project_type import ProjectType
from dataio.data_io_exception import AddObjectException, AddModelAlterationException
from businessclasses.model_catalog_exception import InvalidModelPathException


class TestModelDataIO(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.model_catalog_data_io = ModelCatalogDbDataIo(self.config)
        self.model_data_io = ModelDataIo(self.config, self.model_catalog_data_io)
        self.field_names = ["Model_ID", "Simulation_ID", "Storm_ID", "Dev_Scenario_ID", "Sim_Desc"]

        self.mock_model_alt_bc = mock.MagicMock(spec = ModelAltBc)
        self.mock_model_alt_hydrologic = mock.MagicMock(spec = ModelAltHydrologic)
        self.mock_model_alt_hydraulic = mock.MagicMock(spec = ModelAltHydraulic)
        self.generic_field_attribute_lookup = OrderedDict()
        self.generic_field_attribute_lookup["Generic_ID"] = "id"
        self.generic_field_attribute_lookup["Generic_Domain_ID"] = "generic_domain_id"

        self.mock_model_alt_bc.input_field_attribute_lookup = self.generic_field_attribute_lookup
        self.mock_model_alt_bc.name = "model_alt_bc"
        self.mock_model_alt_hydrologic.input_field_attribute_lookup = self.generic_field_attribute_lookup
        self.mock_model_alt_hydrologic.name = "model_alt_hydrologic"
        self.mock_model_alt_hydraulic.input_field_attribute_lookup = self.generic_field_attribute_lookup
        self.mock_model_alt_hydraulic.name = "model_alt_hydraulic"

        self.mock_simulation = mock.MagicMock(spec = Simulation)
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
        self.mock_simulation.input_field_attribute_lookup = field_attribute_lookup

        self.mock_project_type = mock.MagicMock(spec = ProjectType)
        self.mock_project_type.input_field_attribute_lookup = self.generic_field_attribute_lookup

        self.mock_object_data_io = mock.Mock()
        self.mock_object_data_io.db_data_io.retrieve_current_id.return_value = 1

        self.mock_model = mock.MagicMock(spec = Model)
        self.mock_model.model_path = r"C:\model_path"
        self.mock_model.object_data_io = self.mock_object_data_io
        self.mock_model.id = 11
        self.mock_model.valid = True
        self.mock_model.simulations = [self.mock_simulation]
        self.mock_model.project_types = [self.mock_project_type]
        #TODO: This needs a date-time object
        self.mock_model.create_date = "create_date"
        self.mock_model.model_purpose_id = 1

        self.mock_insert_cursor_object = mock.MagicMock(spec = arcpy.da.InsertCursor)
        self.mock_search_cursor_object = mock.MagicMock(spec = arcpy.da.SearchCursor)
        self.mock_search_cursor_object.__iter__.return_value = iter([["geom"]])

        self.patch_dissolve = mock.patch("arcpy.Dissolve_management")
        self.mock_dissolve = self.patch_dissolve.start()

        self.patch_insert_cursor = mock.patch("arcpy.da.InsertCursor")
        self.mock_insert_cursor = self.patch_insert_cursor.start()

        self.patch_search_cursor = mock.patch("arcpy.da.SearchCursor")
        self.mock_search_cursor = self.patch_search_cursor.start()
        self.mock_search_cursor.return_value = self.mock_search_cursor_object

        self.patch_retrieve_current_simulation_id = mock.patch("dataio.model_catalog_db_data_io.ModelCatalogDbDataIo.retrieve_current_simulation_id")
        self.mock_retrieve_current_simulation_id = self.patch_retrieve_current_simulation_id.start()
        self.mock_retrieve_current_simulation_id.return_value = 1

        self.patch_add_object = mock.patch.object(self.model_data_io, "add_object")
        self.mock_add_object = self.patch_add_object.start()

        self.mock_model.simulations = [self.mock_simulation]
        self.mock_model.model_alterations = [self.mock_model_alt_bc]

        self.patch_os_walk = mock.patch("os.walk")
        self.mock_os_walk = self.patch_os_walk.start()

        self.patch_os_chmod = mock.patch("os.chmod")
        self.mock_os_chmod = self.patch_os_chmod.start()

        self.patch_open = mock.patch("__builtin__.open")
        self.mock_open = self.patch_open.start()

#        self.patch_close = mock.patch("__builtin__.close")
#        self.mock_close = self.patch_close.start()

        self.patch_json_dump = mock.patch("json.dump")
        self.mock_json_dump = self.patch_json_dump.start()

        self.patch_valid_emgaats_model_structure = mock.patch.object(self.mock_model, "valid_emgaats_model_structure")
        self.mock_valid_emgaats_model_structure = self.patch_valid_emgaats_model_structure.start()
        self.mock_valid_emgaats_model_structure.return_value = True

    def tearDown(self):
        self.mock_dissolve = self.patch_dissolve.stop()
        self.mock_insert_cursor = self.patch_insert_cursor.stop()
        self.mock_search_cursor = self.patch_search_cursor.stop()
        self.mock_retrieve_current_simulation_id = self.patch_retrieve_current_simulation_id.stop()
        self.mock_add_object = self.patch_add_object.stop()
        self.mock_os_walk = self.patch_os_walk.stop()
        self.mock_os_chmod = self.patch_os_chmod.stop()
        self.mock_open = self.patch_open.stop()
#        self.mock_close = self.patch_close.stop()
        self.mock_json_dump = self.patch_json_dump.stop()
        self.mock_valid_emgaats_model_structure = self.patch_valid_emgaats_model_structure.stop()

    def test_read_simulations_calls_os_walk(self):
        self.model_data_io.read_simulations(self.mock_model)
        self.assertTrue(self.mock_os_walk.called)

    def test_read_simulation_reads_standard_simulation_existing_scenario_returns_simulation_object(self):
        self.mock_os_walk.return_value = iter([("path", ["D25yr6h"], "file name")])
        list_of_simulations = self.model_data_io.read_simulations(self.mock_model)
        first_simulation = list_of_simulations[0]  # type: Simulation
        self.assertEquals(first_simulation.model_path, r"C:\model_path")
        self.assertEquals(first_simulation.dev_scenario_id, 0)
        self.assertEquals(first_simulation.storm_id, 1)
        self.assertEquals(first_simulation.sim_desc, "D25yr6h")

    def test_read_simulation_reads_standard_simulation_build_out_scenario_returns_simulation_object(self):
        self.mock_os_walk.return_value = iter([("path", ["D25yr6h-BO"], "file name")])
        list_of_simulations = self.model_data_io.read_simulations(self.mock_model)
        first_simulation = list_of_simulations[0]  # type: Simulation
        self.assertEquals(first_simulation.model_path, r"C:\model_path")
        self.assertEquals(first_simulation.dev_scenario_id, 2)
        self.assertEquals(first_simulation.storm_id, 1)
        self.assertEquals(first_simulation.sim_desc, "D25yr6h-BO")

    def test_read_simulation_reads_list_of_simulations_and_returns_correct_simulation_objects(self):
        self.mock_os_walk.return_value = iter([("path", ["D25yr6h-BO","D10yr6h"], "file name")])
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

    def test_read_simulation_reads_user_defined_simulation_returns_simulation_object(self):
        self.mock_os_walk.return_value = iter([("path", ["Dec2015"], "file name")])
        list_of_simulations = self.model_data_io.read_simulations(self.mock_model)
        first_simulation = list_of_simulations[0]  # type: Simulation
        self.assertEquals(first_simulation.model_path, r"C:\model_path")
        self.assertEquals(first_simulation.dev_scenario_id, 0)
        self.assertEquals(first_simulation.storm_id, 0)
        self.assertEquals(first_simulation.sim_desc, "Dec2015")

    def test_add_simulation_calls_add_object_with_correct_arguments(self):
        self.model_data_io.add_simulation(11, self.mock_simulation)
        self.mock_add_object.assert_called_with(11, self.mock_simulation, self.mock_simulation.input_field_attribute_lookup,
                                                self.config.simulation_sde_path)

    def test_create_model_geometry_calls_arcpy_dissolve_management_with_the_correct_arguments(self):
        self.model_data_io.create_model_geometry(self.mock_model)
        input = "C:\model_path" + "\\" + "EmgaatsModel.gdb" + "\\Network\\Links"
        self.mock_dissolve.assert_called_with(input, "in_memory\\Links", "", "", "MULTI_PART")

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

    def test_add_model_alteration_add_object_raises_exception_raises_add_model_alteration_exception(self):
        self.mock_add_object.side_effect = AddObjectException()
        with self.assertRaises((Exception, AddModelAlterationException)):
            self.model_data_io.add_model_alteration(11, self.mock_model_alt_hydraulic)

    def test_add_simulations_calls_add_simulation_with_correct_arguments(self):
        patch_add_simulation = mock.patch.object(self.model_data_io, "add_simulation")
        mock_add_simulation = patch_add_simulation.start()
        self.model_data_io.add_simulations(self.mock_model)
        mock_add_simulation.assert_called_with(11, self.mock_simulation)
        patch_add_simulation.stop()

    def test_add_model_alterations_calls_add_model_alteration_with_correct_arguments(self):
        patch_add_model_alteration = mock.patch.object(self.model_data_io, "add_model_alteration")
        mock_add_model_alteration = patch_add_model_alteration.start()
        self.model_data_io.add_model_alterations(self.mock_model)
        mock_add_model_alteration.assert_called_with(11, self.mock_model_alt_bc)
        patch_add_model_alteration.stop()

    def test_add_project_type_calls_add_object_with_correct_arguments(self):
        with mock.patch.object(self.model_data_io, "add_object") as mock_add_object:
            self.model_data_io.add_project_type(11, self.mock_project_type)
            mock_add_object.assert_called_with(11, self.mock_project_type,
                                               self.generic_field_attribute_lookup, self.config.project_type_sde_path)

    def test_add_project_types_calls_add_project_type_with_correct_arguments(self):
        patch_add_project_type = mock.patch.object(self.model_data_io, "add_project_type")
        mock_add_project_type = patch_add_project_type.start()
        self.model_data_io.add_project_types(self.mock_model)
        mock_add_project_type.assert_called_with(11, self.mock_project_type)
        patch_add_project_type.stop()

    def test_set_registered_model_to_read_only_calls_os_walk_with_correct_arguments(self):
        self.model_data_io.set_registered_model_to_read_only(self.mock_model)
        self.mock_os_walk.assert_called_with(r"C:\model_path")

    def test_set_registered_model_to_read_only_calls_os_path_join_with_correct_arguments(self):
        with mock.patch("os.path.join") as mock_os_path_join:
            self.mock_os_walk.return_value = [["root", "directories", ["filenames"]]]
            self.model_data_io.set_registered_model_to_read_only(self.mock_model)
            mock_os_path_join.assert_called_with("root", "filenames")

    def test_set_registered_model_to_read_only_calls_chmod_with_correct_arguments(self):
        with mock.patch("os.path.join") as mock_os_path_join:
            self.mock_os_walk.return_value = [["root", "directories", ["filenames"]]]
            mock_os_path_join.return_value = "filepath"
            self.model_data_io.set_registered_model_to_read_only(self.mock_model)
            self.mock_os_chmod.assert_called_with("filepath", S_IREAD | S_IRGRP | S_IROTH)

    def test_set_registered_model_to_read_only_calls_valid_emgaats_model_structure(self):
        with mock.patch("os.path.join") as mock_os_path_join:
            self.mock_os_walk.return_value = [["root", "directories", ["filenames"]]]
            mock_os_path_join.return_value = "filepath"
            self.model_data_io.set_registered_model_to_read_only(self.mock_model)
            self.assertTrue(self.mock_valid_emgaats_model_structure.called)

    def test_set_registered_model_to_read_only_invalid_emgaats_model_structure_raises_exception(self):
        with mock.patch("os.path.join") as mock_os_path_join:
            self.mock_os_walk.return_value = [["root", "directories", ["filenames"]]]
            mock_os_path_join.return_value = "filepath"
            self.mock_valid_emgaats_model_structure.return_value = False
            with self.assertRaises((Exception, InvalidModelPathException)):
                self.model_data_io.set_registered_model_to_read_only(self.mock_model)

    def test_set_registered_model_to_read_only_invalid_emgaats_model_structure_chmod_not_called(self):
        with mock.patch("os.path.join") as mock_os_path_join:
            self.mock_os_walk.return_value = [["root", "directories", ["filenames"]]]
            mock_os_path_join.return_value = "filepath"
            self.mock_valid_emgaats_model_structure.return_value = False
            try:
                self.model_data_io.set_registered_model_to_read_only(self.mock_model)
            except:
                pass
            self.assertFalse(self.mock_os_chmod.called)

    # TODO: figure out how to mock/patch create_date with date-time object, see below TODO
    # def test_write_model_registration_file_calls_open_with_correct_arguments(self):
    #     file_path = self.mock_model.model_path
    #     file_name = "model_registration.json"
    #     model_registration_file = file_path + "\\" + file_name
    #     self.model_data_io.write_model_registration_file(self.mock_model)
    #     self.mock_open.assert_called_with(model_registration_file, "w")

    # TODO: figure out how to mock/patch "with" and open(), close()
    # def test_write_model_registration_file_calls_json_dump_with_correct_arguments(self):
    #
    #     self.mock_open.return_value = "filepath"
    #     model_registration_data = {"id": self.mock_model.id, "create_date": self.mock_model.create_date,
    #                                "model_purpose_id": self.mock_model.model_purpose_id,
    #                                "model_purpose": self.config.model_purpose[self.mock_model.model_purpose_id]}
    #     self.model_data_io.write_model_registration_file(self.mock_model)
    #     self.mock_json_dump.assert_called_with(model_registration_data, "filepath")


