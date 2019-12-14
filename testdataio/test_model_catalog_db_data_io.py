from unittest import TestCase
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
import mock
from businessclasses.model_catalog import ModelCatalog
from businessclasses.model import Model
from businessclasses.simulation import Simulation
from businessclasses.model_alteration import ModelAlteration
import arcpy
from testbusinessclasses.mock_config import MockConfig
from dataio.model_data_io import ModelDataIo
from dataio.simulation_data_io import SimulationDataIo

class TestModelCatalogDbDataIO(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.model_catalog_db_data_io = ModelCatalogDbDataIo(self.config)
        self.model_catalog = mock.MagicMock(ModelCatalog)
        self.model = mock.MagicMock(Model)
        self.model_data_io = ModelDataIo(self.config, self.model_catalog_db_data_io)
        self.simulation_data_io = SimulationDataIo(self.config, self.model_catalog_db_data_io)
        self.model.model_id = 0
        self.model.parent_model_id = 0
        self.model.model_request_id = 0
        self.model.project_phase_id = None
        self.model.engine_type_id = None
        self.model.create_date = None
        self.model.deploy_date = None
        self.model.run_date = None
        self.model.extract_date = None
        self.model.created_by = None
        self.model.model_path = None
        self.model.project_type_id = None
        self.model.model_purpose_id = None
        self.model.model_calibration_file = None
        self.model.model_status_id = self.config.model_status_id["Final"]
        self.model.model_alteration_file = None
        self.model.project_num = None
        self.model.model_geometry = None


        self.mock_update_cursor = mock.MagicMock(arcpy.da.UpdateCursor)
        self.mock_update_cursor.__iter__.return_value = iter([("Model", 44), ("Simulation", 55), ("ModelAlteration", 66)])
        self.patch_da_UpdateCursor = mock.patch("arcpy.da.UpdateCursor")
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.start()

        self.patch_da_InsertCursor = mock.patch("arcpy.da.InsertCursor")
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.start()

        self.patch_append_object_to_db = mock.patch.object(self.model_catalog_db_data_io, "append_object_to_db")
        self.mock_append_object_to_db = self.patch_append_object_to_db.start()

        self.patch_read_simulations = mock.patch("dataio.model_data_io.ModelDataIo.read_simulations")
        self.mock_read_simulations = self.patch_read_simulations.start()

        self.patch_append_simulations = mock.patch("dataio.model_data_io.ModelDataIo.append_simulations")
        self.mock_append_simulations = self.patch_append_simulations.start()

        self.patch_append_model_alterations = mock.patch("dataio.model_data_io.ModelDataIo.append_model_alterations")
        self.mock_append_model_alterations = self.patch_append_model_alterations.start()

        self.patch_append_project_types = mock.patch("dataio.model_data_io.ModelDataIo.append_project_types")
        self.mock_append_project_types = self.patch_append_project_types.start()

        self.patch_start_editing_session = mock.patch("dataio.model_data_io.ModelDataIo.start_editing_session")
        self.mock_start_editing_session = self.patch_start_editing_session.start()

        self.mock_start_editing_session.return_value = "editor"

        self.patch_stop_editing_session = mock.patch("dataio.model_data_io.ModelDataIo.stop_editing_session")
        self.mock_stop_editing_session = self.patch_stop_editing_session.start()

        self.patch_set_registered_model_to_read_only = mock.patch("dataio.model_data_io.ModelDataIo.set_registered_model_to_read_only")
        self.mock_set_registered_model_to_read_only = self.patch_set_registered_model_to_read_only.start()

        self.patch_write_model_registration_file = mock.patch("dataio.model_data_io.ModelDataIo.write_model_registration_file")
        self.mock_write_model_registration_file = self.patch_write_model_registration_file.start()

        self.patch_append_model_network = mock.patch("dataio.model_data_io.ModelDataIo.append_model_network")
        self.mock_append_model_network = self.patch_append_model_network.start()

        self.patch_append_simulation_results = mock.patch("dataio.simulation_data_io.SimulationDataIo.append_simulation_results")
        self.mock_append_simulation_results = self.patch_append_simulation_results.start()

    def tearDown(self):
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.stop()
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.stop()
        self.mock_append_object_to_db = self.patch_append_object_to_db.stop()
        self.mock_read_simulations = self.patch_read_simulations.stop()
        self.mock_append_simulations = self.patch_append_simulations.stop()
        self.mock_add_model_alterations = self.patch_append_model_alterations.stop()
        self.mock_append_project_types = self.patch_append_project_types.stop()
        self.mock_start_editing_session = self.patch_start_editing_session.stop()
        self.mock_stop_editing_session = self.patch_stop_editing_session.stop()
        self.mock_set_registered_model_to_read_only = self.patch_set_registered_model_to_read_only.stop()
        self.mock_write_model_registration_file = self.patch_write_model_registration_file.stop()
        self.mock_append_simulation_results = self.patch_append_simulation_results.stop()

    def test_retrieve_current_model_id(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_model_id = self.model_catalog_db_data_io.retrieve_current_model_id()
        self.assertTrue(current_model_id == 44)

    def test_retrieve_current_simulation_id(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_simulation_id = self.model_catalog_db_data_io.retrieve_current_simulation_id()
        self.assertTrue(current_simulation_id == 55)

    def test_retrieve_current_model_alteration_id(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_model_alteration_id = self.model_catalog_db_data_io.retrieve_current_model_alteration_id()
        self.assertTrue(current_model_alteration_id == 66)

    def test_add_model_calls_append_simulations_with_correct_arguments(self):
        self.model_catalog_db_data_io.add_model(self.model, self.model_data_io, self.simulation_data_io)
        self.mock_append_simulations.assert_called_with(self.model)

    def test_add_model_calls_append_model_alterations_with_correct_arguments(self):
        self.model_catalog_db_data_io.add_model(self.model, self.model_data_io, self.simulation_data_io)
        self.mock_append_model_alterations.assert_called_with(self.model)

    def test_add_model_calls_append_project_types_with_correct_arguments(self):
        self.model_catalog_db_data_io.add_model(self.model, self.model_data_io,self.simulation_data_io)
        self.mock_append_project_types.assert_called_with(self.model)

    def test_add_model_calls_start_editing_session_with_correct_workspace(self):
        self.model_catalog_db_data_io.add_model(self.model, self.model_data_io,self.simulation_data_io)
        self.mock_start_editing_session.assert_called_with(self.config.model_catalog_sde_path)

    def test_add_model_calls_stop_editing_session_no_exception_with_save_changes_true(self):
        self.model_catalog_db_data_io.add_model(self.model, self.model_data_io, self.simulation_data_io)
        save_changes = True
        self.mock_stop_editing_session.assert_called_with("editor", save_changes)

    # this test will cause a traceback with an exception. it is testing the rollback.
    def test_add_model_calls_stop_editing_session_exception_thrown_with_save_changes_false(self):
        self.mock_append_simulations.side_effect = Exception()
        save_changes = False
        try:
            self.model_catalog_db_data_io.add_model(self.model, self.model_data_io, self.simulation_data_io)
        except:
            self.mock_stop_editing_session.assert_called_with("editor", save_changes)

    def test_add_model_calls_set_registered_model_to_read_only_with_correct_arguments(self):
        self.model_catalog_db_data_io.add_model(self.model, self.model_data_io, self.simulation_data_io)
        self.mock_set_registered_model_to_read_only.assert_called_with(self.model)

    def test_add_model_calls_write_model_registration_file_with_correct_arguments(self):
        self.model_catalog_db_data_io.add_model(self.model, self.model_data_io, self.simulation_data_io)
        self.mock_write_model_registration_file.assert_called_with(self.model)

    def test_add_model_model_status_is_set_to_final_set_registered_model_to_read_only_called(self):
        self.model_catalog_db_data_io.add_model(self.model, self.model_data_io, self.simulation_data_io)
        self.assertTrue(self.mock_set_registered_model_to_read_only.called)

    def test_add_model_model_status_is_set_to_working_set_registered_model_to_read_only_not_called(self):
        self.model.model_status_id = self.config.model_status_id["Working"]
        self.model_catalog_db_data_io.add_model(self.model, self.model_data_io, self.simulation_data_io)
        self.assertFalse(self.mock_set_registered_model_to_read_only.called)






