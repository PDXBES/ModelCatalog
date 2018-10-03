from unittest import TestCase
from rehab import Rehab
from mock_config import MockConfig
import mock
from pipe import Pipe
import datetime

class TestRehab(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.rehab = Rehab(self.config)

        self.rehab.id = 1
        self.rehab.extract_date = datetime.datetime.today()
        self.rehab.last_inspection_date = datetime.datetime.today()
        self.rehab.purpose = "purpose"

        self.pipe = Pipe()
        self.pipe.asmrecommendedaction = "SP"
        self.pipe.apw = 1
        self.pipe.apwspot = 3
        self.pipe.bpw = 2
        self.pipe.asmrecommendednbcr = 5


    def test_valid_rehab_has_id_extract_date_last_inspection_date_purpose_returns_true(self):
        is_valid = self.rehab.valid
        self.assertTrue(is_valid)

    def test_valid_rehab_has_invalid_id_returns_false(self):
        self.rehab.id = "one"
        is_valid = self.rehab.valid
        self.assertFalse(is_valid)

    def test_valid_rehab_has_invalid_extract_date_returns_false(self):
        self.rehab.extract_date = "date"
        is_valid = self.rehab.valid
        self.assertFalse(is_valid)

    def test_valid_rehab_has_invalid_last_inspection_date_returns_false(self):
        self.rehab.last_inspection_date = "date"
        is_valid = self.rehab.valid
        self.assertFalse(is_valid)

    def test_valid_rehab_has_invalid_purpose_returns_false(self):
        self.rehab.purpose = None
        is_valid = self.rehab.valid
        self.assertFalse(is_valid)

    # def test_calculate_apw_calls_calculate_apw(self):
    #     with mock.patch.object(self.pipe, "calculate_apw") as mock_calculate_apw:
    #         self.rehab.pipes.append(self.pipe)
    #         mock_calculate_apw.return_value = 3
    #         self.rehab.calculate_apw()
    #         rehab_apw = self.rehab.pipes[0].apw
    #         self.assertEquals(rehab_apw, 3)

    #def test_calculate_apw_calls_calculate_capital_cost(self):

