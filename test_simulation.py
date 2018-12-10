from unittest import TestCase
from simulation import Simulation
import mock
from mock_config import MockConfig
from db_data_io import DbDataIo
from generic_class_factory import GenericClassFactory
from collections import OrderedDict
from area import Area

class TestSimulation(TestCase):
    def setUp(self):
        model_path = "String"
        mock_config = MockConfig()
        generic_class_factory = GenericClassFactory(mock_config)
        self.db_data_io = DbDataIo(mock_config, generic_class_factory)
        self.config = mock_config.config
        self.simulation = Simulation(self.config)
        self.simulation.model_path = model_path
        self.simulation.storm_id = 1
        self.simulation.dev_scenario_id = 1

        self.patch_area_field_attribute_lookup = mock.patch("area.Area.field_attribute_lookup")
        self.mock_area_field_attribute_lookup = self.patch_area_field_attribute_lookup.start()

        self.patch_create_objects_from_table = mock.patch("db_data_io.DbDataIo.create_objects_from_table")
        self.mock_create_objects_from_table = self.patch_create_objects_from_table.start()

        self.field_attribute_lookup_create_object = OrderedDict()
        self.field_attribute_lookup_create_object["id_db"] = "id"
        self.field_attribute_lookup_create_object["parent_id_db"] = "parent_id"

    def tearDown(self):
        self.mock_create_objects_from_table = self.patch_create_objects_from_table.stop()
        self.mock_area_field_attribute_lookup = self.patch_area_field_attribute_lookup.stop()



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

    def test_simulation_path_built_for_user_defined_storm(self):
        self.simulation.storm_id = 0
        self.simulation.sim_desc = "test_u_sim"
        path = "String" + "\\" + "sim\\" + "test_u_sim"
        sim_path = self.simulation.path()
        self.assertEquals(sim_path, path)

    def test_create_areas_calls_create_objects_from_table_with_correct_arguments(self):
        input_table = "table"
        self.mock_area_field_attribute_lookup.return_value = "area_field_attribute_lookup"
        self.simulation.create_areas(self.db_data_io)
        self.mock_create_objects_from_table.assert_called_with("table", "area", "area_field_attribute_lookup")