import mock
from unittest import TestCase
from businessclasses.mapping_basis import MappingBasis
from mock_config import MockConfig
from businessclasses.mapping_snapshot import MappingSnapshot

class TestMappingBasis(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.mapping_basis = MappingBasis(self.config)

        self.mock_mapping_snapshot = mock.MagicMock(MappingSnapshot)
        self.mock_mapping_snapshot.valid = True

    def test_add_mapping_snapshot_valid_snapshot_added_to_mapping_basis(self):
        self.mapping_basis.add_mapping_snapshot(self.mock_mapping_snapshot)
        self.assertEquals(self.mapping_basis.mapping_snapshots[0], self.mock_mapping_snapshot)