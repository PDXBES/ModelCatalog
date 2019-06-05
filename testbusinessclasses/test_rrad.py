import mock
from unittest import TestCase
from testbusinessclasses.mock_config import MockConfig
from businessclasses.rrad import Rrad
from dataio.rrad_db_data_io import RradDbDataIo


class TestRrad(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.rrad = Rrad(self.config)

        self.patch_initialize_current_id = mock.patch("businessclasses.rehab.Rehab.initialize_with_current_id")
        self.mock_initialize_current_id = self.patch_initialize_current_id.start()

        self.mock_rrad_db_data_io = mock.MagicMock(RradDbDataIo)

        #self.patch_datetime_datetime_today = mock.patch("datetime.today")
        #self.mock_datetime_datetime_today = self.patch_datetime_datetime_today.start()

    def tearDown(self):
        self.mock_initialize_current_id = self.patch_initialize_current_id.stop()
        #self.mock_datetime_datetime_today = self.patch_datetime_datetime_today.stop()


    def test_create_rehab_for_characterization_calls_initialize_current_id_with_correct_arguments(self):
        self.rrad.create_rehab_for_characterization(self.mock_rrad_db_data_io)
        self.mock_initialize_current_id.assert_called_with(self.config, self.mock_rrad_db_data_io)

    def test_create_rehab_for_characterization_creates_rehab_object_for_purpose_of_characterization(self):
        rehab = self.rrad.create_rehab_for_characterization(self.mock_rrad_db_data_io)
        self.assertEquals(rehab.purpose, "Characterization")

