from unittest import TestCase
from businessclasses.simulation import Simulation
import mock
from mock_config import MockConfig
from dataio.db_data_io import DbDataIo
from collections import OrderedDict
from dataio.simulation_data_io import SimulationDataIo
from businessclasses.area_results import AreaResults
from businessclasses.model import Model

class TestSimulation(TestCase):
    def setUp(self):
        model_path = "String"
        mock_config = MockConfig()
        self.db_data_io = DbDataIo(mock_config)
        self.config = mock_config.config
        self.simulation = Simulation(self.config)
        self.simulation.model_path = model_path
        self.simulation.storm_id = 1
        self.simulation.dev_scenario_id = 1
        self.simulation_data_io = SimulationDataIo(mock_config, self.db_data_io)
        self.mock_model = mock.MagicMock(Model)
        area1 = AreaResults(mock_config)
        area2 = AreaResults(mock_config)
        self.mock_areas = [area1, area2]
        self.simulation.areas = self.mock_areas

        self.patch_area_field_attribute_lookup = mock.patch("businessclasses.area.Area.input_field_attribute_lookup")
        self.mock_area_field_attribute_lookup = self.patch_area_field_attribute_lookup.start()

        self.patch_create_objects_from_table_with_current_id = mock.patch("dataio.db_data_io.DbDataIo.create_objects_from_table_with_current_id")
        self.mock_create_objects_from_table_with_current_id = self.patch_create_objects_from_table_with_current_id.start()
        self.mock_create_objects_from_table_with_current_id.return_value = self.mock_areas

        self.patch_copy_area_results_to_memory = mock.patch("dataio.simulation_data_io.SimulationDataIo.copy_area_results_to_memory")
        self.mock_copy_area_results_to_memory = self.patch_copy_area_results_to_memory.start()

        self.patch_delete_management = mock.patch("arcpy.Delete_management")
        self.mock_delete_management = self.patch_delete_management.start()

        self.patch_os_path_exists = mock.patch("os.path.exists")
        self.mock_os_path_exists = self.patch_os_path_exists.start()

        self.field_attribute_lookup_create_object = OrderedDict()
        self.field_attribute_lookup_create_object["id_db"] = "id"
        self.field_attribute_lookup_create_object["parent_id_db"] = "parent_id"

    def tearDown(self):
        self.mock_create_objects_from_table_with_current_id = self.patch_create_objects_from_table_with_current_id.stop()
        self.mock_area_field_attribute_lookup = self.patch_area_field_attribute_lookup.stop()
        self.mock_copy_area_results_to_memory = self.patch_copy_area_results_to_memory.stop()
        self.mock_delete_management = self.patch_delete_management.stop()
        self.mock_os_path_exists = self.patch_os_path_exists.stop()

    def test_has_results_check_sim_folder_has_results(self):
        self.simulation.has_results()
        self.assertTrue(self.mock_os_path_exists.called)

    def test_has_results_called_with_correct_arguments_for_existing_scenario(self):
        self.simulation.dev_scenario_id = 0
        self.simulation.has_results()
        path = "String" + "\\" + "sim\\" + "D25yr6h"
        self.mock_os_path_exists.assert_called_with(path)

    def test_has_results_called_with_correct_arguments_for_BO_scenario(self):
        self.simulation.dev_scenario_id = 2
        self.simulation.has_results()
        path = "String" + "\\" + "sim\\" + "D25yr6h" + "-BO"
        self.mock_os_path_exists.assert_called_with(path)

    def test_has_results_results_gdb_exists_return_true(self):
        self.mock_os_path_exists.return_value = True
        is_valid = self.simulation.has_results()
        self.assertTrue(is_valid)

    def test_has_results_results_gdb_does_not_exist_return_false(self):
        self.mock_os_path_exists.return_value = False
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

    def test_required_for_model_catalog_required_storm_id_and_dev_scenario_id_returns_true(self):
        self.simulation.storm_id, self.simulation.dev_scenario_id = self.config.ccsp_characterization_storm_and_dev_scenario_ids[0]
        self.mock_model.required_storm_and_dev_scenario_ids.return_value = self.config.ccsp_characterization_storm_and_dev_scenario_ids
        required = self.simulation.required_for_model_catalog(self.mock_model)
        self.assertTrue(required)

    def test_required_for_model_catalog_not_required_storm_id_and_dev_scenario_id_returns_false(self):
        self.mock_model.required_storm_and_dev_scenario_ids.return_value = [(-1,-1)]
        required = self.simulation.required_for_model_catalog(self.mock_model)
        self.assertFalse(required)





