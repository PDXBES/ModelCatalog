import mock
from unittest import TestCase
from testbusinessclasses.mock_config import MockConfig
from businessclasses.mapping_snapshot import MappingSnapshot
from dataio.mapping_basis_data_io import MappingBasisDataIo

class TestMappingBasisDataIo(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.mapping_basis_data_io = MappingBasisDataIo(self.config)

        self.mock_mapping_snapshot = mock.MagicMock(MappingSnapshot)
        self.mock_mapping_snapshot.valid = True

    def test_add_mapping_snapshot_

