import mock
from unittest import TestCase
from testbusinessclasses.mock_config import MockConfig
from businessclasses.mapping_snapshot import MappingSnapshot
from dataio.rrad_mapping_db_data_io import RradMappingDbDataIo
from dataio.mapping_snapshot_data_io import MappingSnapshotDataIo
from businessclasses.model import Model


class TestRradMappingDbDataIo(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.rrad_mapping_db_data_io = RradMappingDbDataIo(self.config)
        self.model = mock.MagicMock(Model)

        self.mock_mapping_snapshot = mock.MagicMock(MappingSnapshot)
        self.mock_mapping_snapshot.valid = True
        self.mock_mapping_snapshot.rehab_id = None

        self.mapping_snapshot_data_io = MappingSnapshotDataIo(self.config, self.rrad_mapping_db_data_io)

        self.patch_start_editing_session = mock.patch("dataio.mapping_snapshot_data_io.MappingSnapshotDataIo.start_editing_session")
        self.mock_start_editing_session = self.patch_start_editing_session.start()

        self.mock_start_editing_session.return_value = "editor"

        self.patch_stop_editing_session = mock.patch("dataio.mapping_snapshot_data_io.MappingSnapshotDataIo.stop_editing_session")
        self.mock_stop_editing_session = self.patch_stop_editing_session.start()

        self.patch_append_object_to_db = mock.patch.object(self.rrad_mapping_db_data_io, "append_object_to_db")
        self.mock_append_object_to_db = self.patch_append_object_to_db.start()

        self.patch_append_mapping_links = mock.patch("dataio.mapping_snapshot_data_io.MappingSnapshotDataIo.append_mapping_links")
        self.mock_append_mapping_links = self.patch_append_mapping_links.start()

        self.patch_append_mapping_nodes = mock.patch(
            "dataio.mapping_snapshot_data_io.MappingSnapshotDataIo.append_mapping_nodes")
        self.mock_append_mapping_nodes = self.patch_append_mapping_nodes.start()

        self.patch_append_mapping_areas = mock.patch(
            "dataio.mapping_snapshot_data_io.MappingSnapshotDataIo.append_mapping_areas")
        self.mock_append_mapping_areas = self.patch_append_mapping_areas.start()

        self.patch_create_mapping_links = mock.patch.object(self.mock_mapping_snapshot, "create_mapping_links")
        self.mock_create_mapping_links = self.patch_create_mapping_links.start()

        self.patch_create_mapping_nodes = mock.patch.object(self.mock_mapping_snapshot, "create_mapping_nodes")
        self.mock_create_mapping_nodes = self.patch_create_mapping_nodes.start()

        self.patch_create_mapping_areas = mock.patch.object(self.mock_mapping_snapshot, "create_mapping_areas")
        self.mock_create_mapping_areas = self.patch_create_mapping_areas.start()

        self.patch_rrad_db_data_io = mock.patch("dataio.rrad_db_data_io.RradDbDataIo")
        self.mock_rrad_db_data_io = self.patch_rrad_db_data_io.start()

        self.patch_create_rehab_snapshot_for_characterization_mapping_snapshot = mock.patch("dataio.rehab_data_io.RehabDataIo.create_rehab_snapshot_for_characterization_mapping_snapshot")
        self.mock_create_rehab_snapshot_for_characterization_mapping_snapshot = self.patch_create_rehab_snapshot_for_characterization_mapping_snapshot.start()
        self.mock_create_rehab_snapshot_for_characterization_mapping_snapshot.return_value = 1

    def tearDown(self):
        self.mock_start_editing_session = self.patch_start_editing_session.stop()
        self.mock_stop_editing_session = self.patch_stop_editing_session.stop()
        self.mock_append_object_to_db = self.patch_append_object_to_db.stop()
        self.mock_append_mapping_links = self.patch_append_mapping_links.stop()
        self.mock_append_mapping_nodes = self.patch_append_mapping_nodes.stop()
        self.mock_append_mapping_areas = self.patch_append_mapping_areas.stop()
        self.mock_create_mapping_links = self.patch_create_mapping_links.stop()
        self.mock_create_mapping_nodes = self.patch_create_mapping_nodes.stop()
        self.mock_create_mapping_areas = self.patch_create_mapping_areas.stop()
        self.mock_rrad_db_data_io = self.patch_rrad_db_data_io.stop()
        self.mock_create_rehab_snapshot_for_characterization_mapping_snapshot = self.patch_create_rehab_snapshot_for_characterization_mapping_snapshot.stop()


    def test_add_mapping_snapshot_calls_create_rehab_snapshot_for_characterization_mapping_snapshot(self):
        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        self.assertTrue(self.mock_create_rehab_snapshot_for_characterization_mapping_snapshot.called)

    def test_add_mapping_snapshot_sets_mapping_snapshot_rehab_id_to_the_correct_value(self):
        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        self.assertEquals(self.mock_mapping_snapshot.rehab_id, 1)

    def test_add_mapping_snapshot_calls_start_editing_session_with_correct_workspace(self):
        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        self.mock_start_editing_session.assert_called_with(self.config.RRAD_MAPPING_sde_path)

    def test_add_mapping_snapshot_append_object_to_db_with_correct_arguments(self):
        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        self.mock_append_object_to_db.assert_called_with(self.mock_mapping_snapshot, MappingSnapshot.input_field_attribute_lookup(),
                                                         "mapping_snapshot_tracking_sde_path", "mapping_snapshot_tracking_sde_path")

    def test_add_mapping_snapshot_no_exceptions_saved_changes_true_stop_editing_session_called_with_correct_arguments(self):
        save_changes = True
        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        self.mock_stop_editing_session.assert_called_with("editor", save_changes)

    # this test will cause a traceback with an exception. it is testing the rollback.
    def test_add_mapping_snapshot_exception_thrown_saved_changes_false_stop_editing_session_called_changes_not_saved_exception_raised(self):
        self.mock_append_object_to_db.side_effect = Exception()
        save_changes = False
        try:
            self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        except:
            self.mock_stop_editing_session.assert_called_with("editor", save_changes)

    def test_add_mapping_snapshot_calls_append_mapping_links_with_correct_arguments(self):
        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        self.mock_append_mapping_links.assert_called_with(self.mock_mapping_snapshot)


    def test_add_mapping_snapshot_calls_append_mapping_nodes_with_correct_arguments(self):
        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        self.mock_append_mapping_nodes.assert_called_with(self.mock_mapping_snapshot)

    def test_add_mapping_snapshot_calls_append_mapping_areas_with_correct_arguments(self):
        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        self.mock_append_mapping_areas.assert_called_with(self.mock_mapping_snapshot)

    def test_add_mapping_snapshot_calls_create_mapping_links_with_correct_arguments(self):
        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        self.mock_create_mapping_links.assert_called_with(self.mapping_snapshot_data_io)

    def test_add_mapping_snapshot_calls_create_mapping_nodes_with_correct_arguments(self):
        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        self.mock_create_mapping_nodes.assert_called_with(self.mapping_snapshot_data_io)

    def test_add_mapping_snapshot_calls_create_mapping_areas_with_correct_arguments(self):
        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        self.mock_create_mapping_areas.assert_called_with(self.mapping_snapshot_data_io)