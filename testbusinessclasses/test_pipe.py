from unittest import TestCase
from businessclasses.rehab_result import RehabResult
import mock
from mock_config import MockConfig


class TestPipe(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.rehab_result = RehabResult(self.config)

    def test_calculate_apw_recommended_action_is_spot(self):
        self.rehab_result.asmrecommendedaction = "SP"
        self.rehab_result.apwspot = 1.11
        self.rehab_result.calculate_apw()
        self.assertAlmostEquals(self.rehab_result.apw, 1.11, 2)

    def test_calculate_apw_recommended_action_is_cipp(self):
        self.rehab_result.asmrecommendedaction = "CIPP"
        self.rehab_result.apwliner = 2.22
        self.rehab_result.calculate_apw()
        self.assertAlmostEquals(self.rehab_result.apw, 2.22, 2)

    def test_calculate_apw_recommended_action_is_oc(self):
        self.rehab_result.asmrecommendedaction = "OC"
        self.rehab_result.apwwhole = 3.33
        self.rehab_result.calculate_apw()
        self.assertAlmostEquals(self.rehab_result.apw, 3.33, 2)

    def test_calculate_apw_recommended_is_not_case_sensitive(self):
        self.rehab_result.asmrecommendedaction = "oc"
        self.rehab_result.apwwhole = 3.33
        self.rehab_result.calculate_apw()
        self.assertAlmostEquals(self.rehab_result.apw, 3.33, 2)

    def test_calculate_capital_cost_calculates_correctly(self):
        self.rehab_result.asmrecommendednbcr = 1.11
        self.rehab_result.apw = 2.22
        self.rehab_result.bpw = 3.33
        self.rehab_result.calculate_capital_cost()
        self.assertAlmostEquals(self.rehab_result.capitalcost, 1, 2)

    def test_is_greater_than_zero_if_input_value_is_not_a_positive_number_return_false(self):
        self.rehab_result.apw = - 0.1
        self.assertEquals(self.rehab_result._is_greater_than_zero(self.rehab_result.apw), False)

    def test_is_greater_than_zero_if_input_value_is_a_positive_number_return_true(self):
        self.rehab_result.apw = 0.1
        self.assertEquals(self.rehab_result._is_greater_than_zero(self.rehab_result.apw), True)

    def test_is_greater_than_zero_if_input_value_is_not_a_number_return_false(self):
        self.rehab_result.apw = "nan"
        self.assertEquals(self.rehab_result._is_greater_than_zero(self.rehab_result.apw), False)

    def test_valid_if_apw_bpw_or_capital_cost_are_not_positive_number_returns_false(self):
        self.rehab_result.apw = -0.01
        self.rehab_result.bpw = 0.1
        self.rehab_result.capitalcost = 0.1
        self.assertEquals(self.rehab_result.valid(), False)
        self.rehab_result.apw = 0.01
        self.rehab_result.bpw = -0.1
        self.rehab_result.capitalcost = 0.1
        self.assertEquals(self.rehab_result.valid(), False)
        self.rehab_result.apw = 0.01
        self.rehab_result.bpw = 0.1
        self.rehab_result.capitalcost = -0.1
        self.assertEquals(self.rehab_result.valid(), False)

    def test_valid_if_apw_bpw_and_capital_cost_are_positive_numbers_returns_true(self):
        self.rehab_result.apw = 0.01
        self.rehab_result.bpw = 0.1
        self.rehab_result.capitalcost = 0.1
        self.rehab_result.asmrecommendedaction = "oc"
        self.rehab_result.asmrecommendednbcr = 1.11
        self.rehab_result.apwwhole = 3.33
        self.assertEquals(self.rehab_result.valid(), True)

    def test_calculate_capital_cost_if_apw_not_greater_than_zero_capital_cost_is_none(self):
        self.rehab_result.apw = 0
        self.rehab_result.bpw = 1
        self.rehab_result.asmrecommendednbcr = 2
        self.rehab_result.calculate_capital_cost()
        self.assertEquals(self.rehab_result.capitalcost, None)

    def test_calculate_capital_cost_if_apw_and_asmrecommendednbcr_is_greater_than_zero_capital_cost_is_calculated(self):
        self.rehab_result.apw = .1
        self.rehab_result.bpw = 1
        self.rehab_result.asmrecommendednbcr = 2
        self.rehab_result.calculate_capital_cost()
        self.assertAlmostEquals(self.rehab_result.capitalcost, .45)

    def test_calculate_capital_cost_if_asmrecommendednbcr_not_greater_than_zero_capital_cost_is_none(self):
        self.rehab_result.apw = 2
        self.rehab_result.bpw = 1
        self.rehab_result.asmrecommendednbcr = 0
        self.rehab_result.calculate_capital_cost()
        self.assertEquals(self.rehab_result.capitalcost, None)

