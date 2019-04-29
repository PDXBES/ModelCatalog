import mock
from unittest import TestCase
from testbusinessclasses.mock_config import MockConfig


class TestMappingSnapshotDataIo(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config


    def tearDown(self):
        pass
