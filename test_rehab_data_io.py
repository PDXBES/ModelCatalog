from unittest import TestCase
from rehab_data_io import RehabDataIO
import mock
from mock_config import MockConfig

class TestRehabDataIO(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.rehab_data_io = RehabDataIO(self.config )

        self.patch_select_by_attribute = mock.patch("arcpy.SelectLayerByAttribute_management")
        self.mock_select_by_attribute = self.patch_select_by_attribute.start()

    def tearDown(self):
        self.mock_select_by_attribute = self.patch_select_by_attribute.stop()

    def test_select_nbcr_data_pipes_calls_select_by_attributes(self):
        self.rehab_data_io.select_nbcr_data_pipes()
        self.assertTrue(self.mock_select_by_attribute.called)

    def test_select_nbcr_data_pipes_called_with_correct_arguments(self):
        self.rehab_data_io.select_nbcr_data_pipes()
        self.mock_select_by_attribute.assert_called_with("rehab_nbcr_data_sde_path", "NEW_SELECTION", "hservstat not in ( 'ABAN' , 'TBAB' , 'DNE' ) and cutno = 0 and compkey is not Null")
