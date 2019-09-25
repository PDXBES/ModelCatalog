from unittest import TestCase
import mock
from businessclasses.simulation import Simulation
from businessclasses.model import Model
from dataio.simulation_data_io import SimulationDataIo
from testbusinessclasses.mock_config import MockConfig
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from businessclasses.area import Area
from dataio.rrad_db_data_io import RradDbDataIo


class TestSimulationDataIO(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        mock_model_catalog_db_data_io = mock.MagicMock(ModelCatalogDbDataIo)
        mock_model_catalog_db_data_io.config = self.config

        self.path = r"c:\temp\fake\sim\D25yr6h\results.gdb\AreaResults"
        self.simulation_data_io = SimulationDataIo(self.config, mock_model_catalog_db_data_io)

        self.patch_simulation_path = mock.patch("businessclasses.simulation.Simulation.path")
        self.mock_simulation_path = self.patch_simulation_path.start()

        self.mock_rrad_db_data_io = mock.MagicMock(RradDbDataIo)

        self.mock_simulation = mock.MagicMock(Simulation)
        self.mock_simulation.storm = "D25yr6h"
        self.mock_simulation.scenario = ""
        self.mock_simulation.id = 1
        self.mock_simulation.storm_id = 22
        self.mock_simulation.dev_scenario_id = 33
        self.mock_simulation.areas = "areas"
        self.mock_simulation.required_for_rrad.return_value = True
        self.mock_simulation.sim_desc = "sim_desc"

        self.patch_create_areas = mock.patch.object(self.mock_simulation, "create_areas")
        self.mock_create_areas = self.patch_create_areas.start()

        self.patch_add_message = mock.patch("arcpy.AddMessage")
        self.mock_add_message = self.patch_add_message.start()

        self.mock_model = mock.MagicMock(Model)
        self.simulation = Simulation(self.config)
        self.patch_simulation_path = mock.patch("businessclasses.simulation.Simulation.path")
        self.mock_simulation_path = self.patch_simulation_path.start()
        self.mock_simulation_path.return_value = self.path

        self.rrad_db_data_io = RradDbDataIo(self.config)

        self.patch_start_editing_session = mock.patch("dataio.simulation_data_io.SimulationDataIo.start_editing_session")
        self.mock_start_editing_session = self.patch_start_editing_session.start()
        self.mock_start_editing_session.return_value = "editor"

        self.patch_stop_editing_session = mock.patch("dataio.simulation_data_io.SimulationDataIo.stop_editing_session")
        self.mock_stop_editing_session = self.patch_stop_editing_session.start()

        self.patch_copy_to_memory = mock.patch("dataio.rrad_db_data_io.RradDbDataIo.copy_to_memory")
        self.mock_copy_to_memory = self.patch_copy_to_memory.start()

        self.patch_add_ids = mock.patch("dataio.rrad_db_data_io.RradDbDataIo.add_ids")
        self.mock_add_ids = self.patch_add_ids.start()

        self.patch_add_parent_id = mock.patch("dataio.rrad_db_data_io.RradDbDataIo.add_parent_id")
        self.mock_add_parent_id = self.patch_add_parent_id.start()

        self.patch_append_objects_to_db = mock.patch("dataio.rrad_db_data_io.RradDbDataIo.append_objects_to_db")
        self.mock_append_objects_to_db = self.patch_append_objects_to_db.start()

        self.patch_append_data_to_db = mock.patch("dataio.rrad_db_data_io.RradDbDataIo.append_table_to_db")
        self.mock_append_data_to_db = self.patch_append_data_to_db.start()

        self.patch_create_feature_class = mock.patch("arcpy.CreateFeatureclass_management")
        self.mock_create_feature_class = self.patch_create_feature_class.start()

    def tearDown(self):
        self.mock_simulation_path = self.patch_simulation_path.stop()

        self.mock_create_areas = self.patch_create_areas.stop()
        self.mock_add_message = self.patch_add_message.stop()
        self.mock_start_editing_session = self.patch_start_editing_session.stop()
        self.mock_stop_editing_session = self.patch_stop_editing_session.stop()
        self.mock_copy_to_memory = self.patch_copy_to_memory.stop()
        self.mock_add_ids = self.patch_add_ids.stop()
        self.mock_add_parent_id = self.patch_add_parent_id.stop()
        self.mock_append_objects_to_db = self.patch_append_objects_to_db.stop()
        self.mock_append_data_to_db = self.patch_append_data_to_db.stop()
        self.mock_create_feature_class = self.patch_create_feature_class.stop()


    def test_area_results_path_creates_correct_path(self):
        self.mock_simulation_path.return_value = r"c:\temp\fake\sim\D25yr6h"
        area_results_path = self.simulation_data_io.area_results_path(self.simulation)
        self.assertEquals(area_results_path, r"c:\temp\fake\sim\D25yr6h\results.gdb\AreaResults")

    def test_link_results_path_creates_correct_path(self):
        self.mock_simulation_path.return_value = r"c:\temp\fake\sim\D25yr6h"
        link_results_path = self.simulation_data_io.link_results_path(self.simulation)
        self.assertEquals(link_results_path, r"c:\temp\fake\sim\D25yr6h\results.gdb\LinkResults")

    def test_node_results_path_creates_correct_path(self):
        self.mock_simulation_path.return_value = r"c:\temp\fake\sim\D25yr6h"
        node_results_path = self.simulation_data_io.node_results_path(self.simulation)
        self.assertEquals(node_results_path, r"c:\temp\fake\sim\D25yr6h\results.gdb\NodeResults")

    def test_node_flooding_results_path_creates_correct_path(self):
        self.mock_simulation_path.return_value = r"c:\temp\fake\sim\D25yr6h"
        node_flooding_results_path = self.simulation_data_io.node_flooding_results_path(self.simulation)
        self.assertEquals(node_flooding_results_path, r"c:\temp\fake\sim\D25yr6h\results.gdb\NodeFloodingResults")

    def test_copy_link_results_to_memory_calls_copy_results_to_memory_with_correct_arguments(self):
        with mock.patch.object(self.simulation_data_io, "copy_results_to_memory") as mock_copy_results:
            with mock.patch.object(self.simulation_data_io, "link_results_path") as mock_link_results_path:
                mock_link_results_path.return_value = "mock_link_results_path"
                output_table_name = "output_table_name"
                self.simulation_data_io.copy_link_results_to_memory(self.mock_simulation, output_table_name, self.rrad_db_data_io)
                mock_copy_results.assert_called_with("mock_link_results_path", output_table_name, self.rrad_db_data_io,
                                                     self.mock_simulation, "rrad_link_id", "link")

    def test_copy_node_results_to_memory_calls_copy_results_to_memory_with_correct_arguments(self):
        with mock.patch.object(self.simulation_data_io, "copy_results_to_memory") as mock_copy_results:
            with mock.patch.object(self.simulation_data_io, "node_results_path") as mock_node_results_path:
                mock_node_results_path.return_value = "mock_node_results_path"
                output_table_name = "output_table_name"
                self.simulation_data_io.copy_node_results_to_memory(self.mock_simulation, output_table_name, self.rrad_db_data_io)
                mock_copy_results.assert_called_with("mock_node_results_path", output_table_name, self.rrad_db_data_io,
                                                     self.mock_simulation, "rrad_node_id", "node")

    def test_copy_node_flooding_results_to_memory_calls_copy_results_to_memory_with_correct_arguments(self):
        with mock.patch.object(self.simulation_data_io, "copy_results_to_memory") as mock_copy_results:
            with mock.patch.object(self.simulation_data_io, "node_flooding_results_path") as mock_node_flooding_results_path:
                mock_node_flooding_results_path.return_value = "mock_node_flooding_results_path"
                output_table_name = "output_table_name"
                self.simulation_data_io.copy_node_flooding_results_to_memory(self.mock_simulation, output_table_name, self.rrad_db_data_io)
                mock_copy_results.assert_called_with("mock_node_flooding_results_path", output_table_name, self.rrad_db_data_io,
                                                     self.mock_simulation, "rrad_node_flooding_id", "node_flooding")

    # TODO create this test
    # def test_copy_area_results_to_memory_calls_copy_results_to_memory_with_correct_arguments(self):
    #     with mock.patch.object(self.simulation_data_io, "copy_results_to_memory") as mock_copy_results:
    #         with mock.patch.object(self.simulation_data_io, "area_results_path") as mock_area_results_path:
    #             mock_area_results_path.return_value = "mock_area_results_path"
    #             output_table_name = "output_table_name"
    #             self.simulation_data_io.copy_area_results_to_memory(self.mock_simulation, output_table_name, self.rrad_db_data_io)
    #             mock_copy_results.assert_called_with("mock_area_results_path", output_table_name, self.rrad_db_data_io,
    #                                                  self.mock_simulation, "rrad_area_id", "area")

    def test_copy_results_to_memory_calls_copy_to_memory_with_correct_arguments(self):
        input_table = "input_table"
        output_table_name = "output_table_name"
        output_table = "in_memory\\output_table_name"
        id_field = "id_field"
        object_type = "object_type"
        self.simulation_data_io.copy_results_to_memory(input_table, output_table_name, self.rrad_db_data_io,
                                                       self.mock_simulation, id_field, object_type)
        self.mock_copy_to_memory.assert_called_with(input_table, output_table_name)

    def test_copy_results_to_memory_calls_add_ids_with_correct_arguments(self):
        input_table = "input_table"
        output_table_name = "output_table_name"
        output_table = "in_memory\\output_table_name"
        id_field = "id_field"
        object_type = "object_type"
        self.simulation_data_io.copy_results_to_memory(input_table, output_table_name, self.rrad_db_data_io,
                                                       self.mock_simulation, id_field, object_type)
        self.mock_add_ids.assert_called_with(output_table, "id_field", "object_type")

    def test_copy_results_to_memory_calls_add_parent_id_with_correct_arguments(self):
        input_table = "input_table"
        output_table_name = "output_table_name"
        output_table = "in_memory\\output_table_name"
        id_field = "id_field"
        object_type = "object_type"
        self.simulation_data_io.copy_results_to_memory(input_table, output_table_name, self.rrad_db_data_io,
                                                       self.mock_simulation, id_field, object_type)
        self.mock_add_parent_id.assert_called_with(output_table, "Simulation_ID", 1)

    def test_append_area_results_to_db_calls_append_table_to_db_with_correct_arguments(self):
        target_path = self.config.area_results_sde_path
        template_path = target_path
        area_results = ["area1", "area2"]
        field_attribute_lookup = Area.input_field_attribute_lookup()
        self.simulation_data_io.append_area_results_to_db(area_results, self.rrad_db_data_io)
        self.mock_append_objects_to_db.assert_called_with(["area1", "area2"], field_attribute_lookup, "area_results_sde_path", "area_results_sde_path")

    def test_append_simulation_results_simulation_required_for_rrad_calls_create_areas_with_correct_arguments(self):
        with mock.patch.object(self.simulation_data_io, "copy_link_results_to_memory"):
            with mock.patch.object(self.simulation_data_io, "copy_node_results_to_memory"):
                with mock.patch.object(self.simulation_data_io, "copy_node_flooding_results_to_memory"):
                        self.simulation_data_io.append_simulation_results(self.mock_simulation, self.mock_model,
                                                                          self.rrad_db_data_io)
                        self.mock_create_areas.assert_called_with(self.simulation_data_io, self.rrad_db_data_io)

    def test_append_simulation_results_simulation_required_for_rrad_calls_start_editing_session_with_correct_workspace(self):
        with mock.patch.object(self.simulation_data_io, "copy_link_results_to_memory"):
            with mock.patch.object(self.simulation_data_io, "copy_node_results_to_memory"):
                with mock.patch.object(self.simulation_data_io, "copy_node_flooding_results_to_memory"):
                    with mock.patch.object(self.simulation_data_io, "append_area_results_to_db"):
                        self.simulation_data_io.append_simulation_results(self.mock_simulation, self.mock_model, self.rrad_db_data_io)
                        self.mock_start_editing_session.assert_called_with("RRAD_sde_path")

    def test_append_simulation_results_simulation_required_for_rrad_calls_copy_to_memory_with_correct_arguments(self):
        with mock.patch.object(self.simulation_data_io, "copy_link_results_to_memory") as mock_copy_link_results_to_memoryt:
            with mock.patch.object(self.simulation_data_io, "copy_node_results_to_memory") as mock_copy_node_results_to_memory:
                with mock.patch.object(self.simulation_data_io, "copy_node_flooding_results_to_memory") as mock_copy_node_flooding_results_to_memory:
                    with mock.patch.object(self.simulation_data_io, "append_area_results_to_db"):
                        self.simulation_data_io.append_simulation_results(self.mock_simulation, self.mock_model, self.rrad_db_data_io)
                        mock_copy_link_results_to_memoryt.assert_called_with(self.mock_simulation, 'link_results_table_name', self.rrad_db_data_io)
                        mock_copy_node_results_to_memory.assert_called_with(self.mock_simulation, 'node_results_table_name', self.rrad_db_data_io)
                        mock_copy_node_flooding_results_to_memory.assert_called_with(self.mock_simulation, 'node_flooding_results_table_name', self.rrad_db_data_io)

    def test_append_simulation_results_simulation_required_for_rrad_calls_append_table_to_db_results_with_correct_arguments(self):
        with mock.patch.object(self.simulation_data_io, "copy_link_results_to_memory"):
            with mock.patch.object(self.simulation_data_io, "copy_node_results_to_memory"):
                with mock.patch.object(self.simulation_data_io, "copy_node_flooding_results_to_memory"):
                    with mock.patch.object(self.simulation_data_io, "append_area_results_to_db"):
                        self.simulation_data_io.append_simulation_results(self.mock_simulation, self.mock_model, self.rrad_db_data_io)
                        self.mock_append_data_to_db.assert_has_calls([mock.call("in_memory\\link_results_table_name", "link_results_sde_path"),
                                                                       mock.call("in_memory\\node_results_table_name", "node_results_sde_path"),
                                                                       mock.call("in_memory\\node_flooding_results_table_name", "node_flooding_results_sde_path")])

    def test_append_simulation_results_simulation_required_for_rrad_calls_append_area_results_with_correct_arguments(self):
        with mock.patch.object(self.simulation_data_io, "copy_link_results_to_memory"):
            with mock.patch.object(self.simulation_data_io, "copy_node_results_to_memory"):
                with mock.patch.object(self.simulation_data_io, "copy_node_flooding_results_to_memory"):
                    with mock.patch.object(self.simulation_data_io, "append_area_results_to_db") as mock_append_area_results:
                        self.simulation_data_io.append_simulation_results(self.mock_simulation, self.mock_model, self.rrad_db_data_io)
                        mock_append_area_results.assert_called_with("areas", self.rrad_db_data_io)

    def test_append_simulation_results_simulation_required_for_rrad_calls_stop_editing_no_exception_saves_changes(self):
        with mock.patch.object(self.simulation_data_io, "copy_link_results_to_memory"):
            with mock.patch.object(self.simulation_data_io, "copy_node_results_to_memory"):
                with mock.patch.object(self.simulation_data_io, "copy_node_flooding_results_to_memory"):
                    with mock.patch.object(self.simulation_data_io, "append_area_results_to_db"):
                        self.simulation_data_io.append_simulation_results(self.mock_simulation, self.mock_model, self.rrad_db_data_io)
                        self.mock_stop_editing_session.assert_called_with("editor", True)

    def test_append_simulation_results_simulation_required_for_rrad_calls_stop_editing_exception_thrown_save_changes_false(self):
        with mock.patch.object(self.simulation_data_io, "copy_link_results_to_memory")as mock_copy_link_results_to_memory:
            with mock.patch.object(self.simulation_data_io, "copy_node_results_to_memory"):
                with mock.patch.object(self.simulation_data_io, "copy_node_flooding_results_to_memory"):
                    with mock.patch.object(self.simulation_data_io, "append_area_results_to_db") as mock_append_area_results_to_db:
                        mock_append_area_results_to_db.side_effect = Exception()
                        try:
                            self.simulation_data_io.append_simulation_results(self.mock_simulation, self.mock_model, self.rrad_db_data_io)
                        except:
                            self.mock_stop_editing_session.assert_called_with("editor", False)

    def test_append_simulation_results_calls_simulation_required_for_rrad_with_correct_arguments(self):
        with mock.patch.object(self.simulation_data_io, "copy_link_results_to_memory"):
            with mock.patch.object(self.simulation_data_io, "copy_node_results_to_memory"):
                with mock.patch.object(self.simulation_data_io, "copy_node_flooding_results_to_memory"):
                    with mock.patch.object(self.simulation_data_io, "append_area_results_to_db"):
                        self.simulation_data_io.append_simulation_results(self.mock_simulation, self.mock_model, self.rrad_db_data_io)
                        self.mock_simulation.required_for_rrad.assert_called_with(self.mock_model)

    def test_append_simulation_results_simulation_not_required_does_not_call_copies_and_append_results_methods(self):
        self.mock_simulation.required_for_rrad.return_value = False
        with mock.patch.object(self.simulation_data_io, "copy_link_results_to_memory") as mock_copy_link_results:
            with mock.patch.object(self.simulation_data_io, "copy_node_results_to_memory") as mock_copy_node_results:
                with mock.patch.object(self.simulation_data_io,
                                       "copy_node_flooding_results_to_memory") as mock_copy_node_flooding_results:
                    with mock.patch.object(self.simulation_data_io,
                                           "append_area_results_to_db") as mock_append_area_results:
                        self.simulation_data_io.append_simulation_results(self.mock_simulation, self.mock_model,
                                                                          self.rrad_db_data_io)
                        self.assertFalse(mock_copy_link_results.called)
                        self.assertFalse(mock_copy_node_results.called)
                        self.assertFalse(mock_copy_node_flooding_results.called)
                        self.assertFalse(mock_append_area_results.called)

    def test_append_simulation_results_simulation_not_required_add_message_called_with_correct_message(self):
        self.mock_simulation.required_for_rrad.return_value = False
        with mock.patch.object(self.simulation_data_io, "copy_link_results_to_memory"):
            with mock.patch.object(self.simulation_data_io, "copy_node_results_to_memory"):
                with mock.patch.object(self.simulation_data_io,
                                       "copy_node_flooding_results_to_memory"):
                    with mock.patch.object(self.simulation_data_io,
                                           "append_area_results_to_db"):
                        self.simulation_data_io.append_simulation_results(self.mock_simulation, self.mock_model,
                                                                          self.mock_rrad_db_data_io)
                        self.mock_add_message.assert_called_with("Simulation: sim_desc is not required for the RRAD.")

    # def test_append_all_simulation_results_calls_create_feature_class_with_correct_arguments(self):
    #     self.simulation_data_io.append_all_simulation_results(self.mock_model, self.rrad_db_data_io)
    #     self.mock_create_feature_class.assert_called_with("in_memory\\")
