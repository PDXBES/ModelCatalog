import mock
from unittest import TestCase
from testbusinessclasses.mock_config import MockConfig
from businessclasses.mapping_snapshot import MappingSnapshot
from dataio.mapping_basis_db_data_io import MappingBasisDbDataIo
from dataio.mapping_snapshot_data_io import MappingSnapshotDataIo
from businessclasses.model import Model


class TestMappingBasisDbDataIo(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.mapping_basis_db_data_io = MappingBasisDbDataIo(self.config)
        self.model = mock.MagicMock(Model)

        self.mock_mapping_snapshot = mock.MagicMock(MappingSnapshot)
        self.mock_mapping_snapshot.valid = True

        self.mapping_snapshot_data_io = MappingSnapshotDataIo(self.config, self.mapping_basis_db_data_io)

        self.patch_start_editing_session = mock.patch("dataio.mapping_snapshot_data_io.MappingSnapshotDataIo.start_editing_session")
        self.mock_start_editing_session = self.patch_start_editing_session.start()

        self.mock_start_editing_session.return_value = "editor"

        self.patch_stop_editing_session = mock.patch("dataio.mapping_snapshot_data_io.MappingSnapshotDataIo.stop_editing_session")
        self.mock_stop_editing_session = self.patch_stop_editing_session.start()

        self.patch_append_object_to_db = mock.patch.object(self.mapping_basis_db_data_io, "append_object_to_db")
        self.mock_append_object_to_db = self.patch_append_object_to_db.start()

    def tearDown(self):
        self.mock_start_editing_session = self.patch_start_editing_session.stop()
        self.mock_stop_editing_session = self.patch_stop_editing_session.stop()
        self.mock_append_object_to_db = self.patch_append_object_to_db.stop()


    def test_add_mapping_snapshot_calls_start_editing_session_with_correct_workspace(self):
        self.mapping_basis_db_data_io.add_mapping_snapshot(self.mock_mapping_snapshot, self.mapping_snapshot_data_io)
        self.mock_start_editing_session.assert_called_with(self.config.RRAD_MAPPING_sde_path)

    def test_add_mapping_snapshot_append_object_to_db_with_correct_arguments(self):
        self.mapping_basis_db_data_io.add_mapping_snapshot(self.model, self.mapping_snapshot_data_io)
        self.mock_append_object_to_db.assert_called_with(self.model, Model.input_field_attribute_lookup(),
                                                         "model_tracking_sde_path", "model_tracking_sde_path")
