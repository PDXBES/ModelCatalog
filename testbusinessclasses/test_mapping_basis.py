import mock
from unittest import TestCase
from businessclasses.mapping_basis import MappingBasis
from mock_config import MockConfig
from businessclasses.mapping_snapshot import MappingSnapshot
from businessclasses.mapping_snapshot_exception import InvalidMappingSnapshotException
from businessclasses.mapping_snapshot_exception import DuplicateMappingSnapshotException

class TestMappingBasis(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.mapping_basis = MappingBasis(self.config)

        self.mock_mapping_snapshot = mock.MagicMock(MappingSnapshot)
        self.mock_mapping_snapshot.valid = True

        self.mock_mapping_snapshot2 = mock.MagicMock(MappingSnapshot)
        self.mock_mapping_snapshot2.valid = True

    def test_add_mapping_snapshot_valid_snapshot_added_to_mapping_basis(self):
        self.mapping_basis.add_mapping_snapshot(self.mock_mapping_snapshot)
        self.assertEquals(self.mapping_basis.mapping_snapshots[0], self.mock_mapping_snapshot)

    def test_add_mapping_snapshot_invalid_snapshot_empty_mapping_basis_snapshot_not_added_to_mapping_basis(self):
        self.mock_mapping_snapshot.valid = False

        with self.assertRaises(InvalidMappingSnapshotException):
            self.mapping_basis.add_mapping_snapshot(self.mock_mapping_snapshot)

        self.assertEquals(len(self.mapping_basis.mapping_snapshots), 0)

    def test_add_mapping_snapshot_invalid_snapshot_not_empty_mapping_basis_snapshot_not_added_to_mapping_basis(self):
        self.mock_mapping_snapshot2.valid = False
        self.mapping_basis.mapping_snapshots.append(self.mock_mapping_snapshot)

        with self.assertRaises(InvalidMappingSnapshotException):
            self.mapping_basis.add_mapping_snapshot(self.mock_mapping_snapshot2)

        self.assertFalse(self.mock_mapping_snapshot2 in self.mapping_basis.mapping_snapshots)

    def test_add_mapping_snapshot_valid_snapshot_in_mapping_basis_duplicate_snapshot_not_added_to_mapping_basis(self):
        self.mapping_basis.mapping_snapshots.append(self.mock_mapping_snapshot)

        with self.assertRaises(DuplicateMappingSnapshotException):
            self.mapping_basis.add_mapping_snapshot(self.mock_mapping_snapshot)

        self.assertEquals(self.mapping_basis.mapping_snapshots.count(self.mock_mapping_snapshot), 1)

    def test_add_mapping_snapshot_invalid_snapshot_raises_invalid_snapshot_exception(self):
        self.mock_mapping_snapshot.valid = False
        with self.assertRaises(InvalidMappingSnapshotException):
            self.mapping_basis.add_mapping_snapshot(self.mock_mapping_snapshot)

    def test_add_mapping_snapshot_valid_snapshot_in_mapping_basis_duplicate_snapshot_raises_duplicate_mapping_snapshot_exception(self):
        self.mapping_basis.mapping_snapshots.append(self.mock_mapping_snapshot)
        with self.assertRaises(DuplicateMappingSnapshotException):
            self.mapping_basis.add_mapping_snapshot(self.mock_mapping_snapshot)
