from unittest import TestCase
import mock, arcpy
from simulation import Simulation
from model import Model
from simulation_data_io import SimulationDataIO
from mock_config import MockConfig
from model_catalog_db_data_io import ModelCatalogDbDataIo
from area import Area


class TestSimulationDataIO(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        mock_model_catalog_db_data_io = mock.MagicMock(ModelCatalogDbDataIo)
        mock_model_catalog_db_data_io.config = self.config

        self.patch_model_catalog_db_data_io_copy = mock.patch.object(mock_model_catalog_db_data_io, "copy")
        self.mock_model_catalog_db_data_io_copy = self.patch_model_catalog_db_data_io_copy.start()

        self.patch_model_catalog_db_data_io_copy_to_memory = mock.patch.object(mock_model_catalog_db_data_io, "copy_to_memory")
        self.mock_model_catalog_db_data_io_copy_to_memory = self.patch_model_catalog_db_data_io_copy_to_memory.start()

        self.path = r"c:\temp\fake\sim\D25yr6h\results.gdb\AreaResults"
        self.simulationdataio = SimulationDataIO(self.config, mock_model_catalog_db_data_io)

        self.patch_append_feature_class_to_db = mock.patch.object(mock_model_catalog_db_data_io, "append_feature_class_to_db")
        self.mock_append_feature_class_to_db = self.patch_append_feature_class_to_db.start()

        self.mock_simulation = mock.MagicMock(Simulation)
        self.mock_simulation.storm = "D25yr6h"
        self.mock_simulation.scenario = ""
        self.mock_simulation.id = 1
        self.mock_simulation.storm_id = 22
        self.mock_simulation.dev_scenario_id = 33
        self.mock_model = mock.MagicMock(Model)
        self.simulation = Simulation(self.config)
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
        self.mock_model_catalog_db_data_io_copy = self.patch_model_catalog_db_data_io_copy.stop()
        self.mock_model_catalog_db_data_io_copy_to_memory = self.patch_model_catalog_db_data_io_copy_to_memory.stop()
        self.mock_append_feature_class_to_db = self.patch_append_feature_class_to_db.stop()

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

    def test_copy_link_results_calls_copy(self):
        self.simulationdataio.copy_link_results(self.mock_simulation)
        self.assertTrue(self.mock_model_catalog_db_data_io_copy.called)


    def test_copy_link_results_calls_copy_with_correct_arguments(self):
        patch_link_results_path = mock.patch.object(self.simulationdataio, "link_results_path")
        mock_link_results_path = patch_link_results_path.start()
        patch_id_to_field_map = mock.patch.object(self.simulationdataio, "_id_to_field_map")
        mock_id_to_field_map = patch_id_to_field_map.start()
        mock_link_results_path.return_value = "link_results_path"
        mock_id_to_field_map.return_value = "id_to_field_map"
        self.simulationdataio.copy_link_results(self.mock_simulation)
        self.mock_model_catalog_db_data_io_copy.assert_called_with("link_results_path", "link_results_sde_path", None, "id_to_field_map")
        patch_link_results_path.stop()
        patch_id_to_field_map.stop()


    def test_copy_node_results_calls_copy(self):
        self.simulationdataio.copy_node_results(self.mock_simulation)
        self.assertTrue(self.mock_model_catalog_db_data_io_copy.called)

    def test_copy_node_results_calls_copy_with_correct_arguments(self):
        patch_node_results_path = mock.patch.object(self.simulationdataio, "node_results_path")
        mock_node_results_path = patch_node_results_path.start()

        patch_id_to_field_map = mock.patch.object(self.simulationdataio, "_id_to_field_map")
        mock_id_to_field_map = patch_id_to_field_map.start()

        mock_node_results_path.return_value = "node_results_path"
        mock_id_to_field_map.return_value = "id_to_field_map"

        self.simulationdataio.copy_node_results(self.mock_simulation)
        self.mock_model_catalog_db_data_io_copy.assert_called_with("node_results_path", "node_results_sde_path", None,
                                                                   "id_to_field_map")

        patch_node_results_path.stop()
        patch_id_to_field_map.stop()

    def test_copy_node_flooding_results_calls_copy(self):
        self.simulationdataio.copy_node_flooding_results(self.mock_simulation)
        self.assertTrue(self.mock_model_catalog_db_data_io_copy.called)

    def test_copy_node_flooding_results_calls_copy_with_correct_arguments(self):
        patch_node_flooding_results_path = mock.patch.object(self.simulationdataio, "node_flooding_results_path")
        mock_node_flooding_results_path = patch_node_flooding_results_path.start()

        patch_id_to_field_map = mock.patch.object(self.simulationdataio, "_id_to_field_map")
        mock_id_to_field_map = patch_id_to_field_map.start()

        mock_node_flooding_results_path.return_value = "node_flooding_results_path"
        mock_id_to_field_map.return_value = "id_to_field_map"

        self.simulationdataio.copy_node_flooding_results(self.mock_simulation)
        self.mock_model_catalog_db_data_io_copy.assert_called_with("node_flooding_results_path", "node_flooding_results_sde_path",
                                                                   None,
                                                                   "id_to_field_map")
        patch_node_flooding_results_path.stop()
        patch_id_to_field_map.stop()

    def test_copy_area_results_calls_copy(self):
        self.simulationdataio.copy_area_results(self.mock_simulation)
        self.assertTrue(self.mock_model_catalog_db_data_io_copy.called)

    def test_copy_area_results_calls_copy_with_correct_arguments(self):
        patch_area_results_path = mock.patch.object(self.simulationdataio, "area_results_path")
        mock_area_results_path = patch_area_results_path.start()

        patch_id_to_field_map = mock.patch.object(self.simulationdataio, "_id_to_field_map")
        mock_id_to_field_map = patch_id_to_field_map.start()

        mock_area_results_path.return_value = "area_results_path"
        mock_id_to_field_map.return_value = "id_to_field_map"

        self.simulationdataio.copy_area_results(self.mock_simulation)
        self.mock_model_catalog_db_data_io_copy.assert_called_with("area_results_path", "area_results_sde_path",
                                                                   None,
                                                                   "id_to_field_map")

        patch_area_results_path.stop()
        patch_id_to_field_map.stop()

    def test_copy_area_results_to_memory_calls_copy_with_correct_arguments(self):
        patch_area_results_path = mock.patch.object(self.simulationdataio, "area_results_path")
        mock_area_results_path = patch_area_results_path.start()

        patch_id_to_field_map = mock.patch.object(self.simulationdataio, "_id_to_field_map")
        mock_id_to_field_map = patch_id_to_field_map.start()

        mock_area_results_path.return_value = "area_results_path"
        mock_id_to_field_map.return_value = "parent_id_to_db_field_mapping"

        self.simulationdataio.copy_area_results_to_memory(self.mock_simulation, "output_table_name")
        self.mock_model_catalog_db_data_io_copy_to_memory.assert_called_with("area_results_path", "output_table_name", "parent_id_to_db_field_mapping")

        patch_area_results_path.stop()
        patch_id_to_field_map.stop()

    def test_append_area_results_to_db_calls_append_table_to_db_with_correct_arguments(self):
        target_path = self.config.area_results_sde_path
        template_path = target_path
        area_results = ["area1", "area2"]
        field_attribute_lookup = Area.output_field_attribute_lookup()
        self.simulationdataio.append_area_results_to_db(area_results)
        self.mock_append_feature_class_to_db.assert_called_with(["area1", "area2"], field_attribute_lookup, "area_results_sde_path", "area_results_sde_path")
