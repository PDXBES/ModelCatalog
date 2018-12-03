from unittest import TestCase
from generic_object import GenericObject
import mock
from mock_config import MockConfig

class TestGenericObject(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.mock_object_data_io = mock.Mock()
        self.mock_object_data_io.db_data_io.retrieve_current_id.return_value = 1
        pass

    def test_initialize_with_current_id_returns_a_generic_object_with_the_current_id(self):
        generic_object_with_id = GenericObject.initialize_with_current_id(self.config, self.mock_object_data_io)
        self.assertEqual(generic_object_with_id.id, 1)
